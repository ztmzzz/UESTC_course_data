package main

import (
	"context"
	"errors"
	"fmt"
	"github.com/gorilla/mux"
	"github.com/tidwall/gjson"
	"google.golang.org/grpc"
	"google.golang.org/grpc/credentials/insecure"
	"hash/fnv"
	pb "homework/kvStore"
	"io"
	"log"
	"net"
	"net/http"
	"os"
	"strconv"
)

func distribute(s string) int {
	h := fnv.New32a()
	if _, err := h.Write([]byte(s)); err != nil {
		return 0
	}
	return int(h.Sum32() % 3)
}

func set(w http.ResponseWriter, r *http.Request) {
	bodyByte, err := io.ReadAll(r.Body)
	if err != nil {
		http.Error(w, err.Error(), http.StatusBadRequest)
		return
	}
	bodyString := string(bodyByte)
	gjson.ForEachLine(bodyString, func(line gjson.Result) bool {
		line.ForEach(func(key, value gjson.Result) bool {
			if distribute(key.Str) == id {
				c.data[key.Str] = value.Raw
			} else {
				client := clientPool[distribute(key.Str)]
				if _, err := client.Set(context.Background(), &pb.SetRequest{Key: key.Str, Value: value.Raw}); err != nil {
					fmt.Println(err)
					return false
				}
			}
			return true
		})
		return true
	})
	w.WriteHeader(http.StatusOK)
}
func get(w http.ResponseWriter, r *http.Request) {
	result := ""
	vars := mux.Vars(r)
	key := vars["key"]
	if distribute(key) == id {
		if value, ok := c.data[key]; ok {
			result = "{\"" + key + "\":" + value + "}"
			w.WriteHeader(http.StatusOK)
		} else {
			w.WriteHeader(http.StatusNotFound)
			return
		}
	} else {
		client := clientPool[distribute(key)]
		res, err := client.Get(context.Background(), &pb.GetRequest{Key: key})
		if err != nil {
			w.WriteHeader(http.StatusNotFound)
			return
		}
		w.WriteHeader(http.StatusOK)
		result = "{\"" + key + "\":" + res.Value + "}"
	}
	if _, err := fmt.Fprint(w, result); err != nil {
		fmt.Println(err)
	}
}
func deleteKey(w http.ResponseWriter, r *http.Request) {
	w.WriteHeader(http.StatusOK) //要求永远返回200
	deleteNum := 0
	vars := mux.Vars(r)
	key := vars["key"]
	if distribute(key) == id {
		if _, ok := c.data[key]; ok {
			delete(c.data, key)
			deleteNum = 1
		}
	} else {
		client := clientPool[distribute(key)]
		res, err := client.Delete(context.Background(), &pb.DeleteRequest{Key: key})
		if err != nil {
			fmt.Println(err)
			return
		}
		if res.Success {
			deleteNum = 1
		}
	}
	if _, err := fmt.Fprint(w, deleteNum); err != nil {
		fmt.Println(err)
		return
	}
}

type kvStoreServer struct {
	pb.UnimplementedKvStoreServer
	data map[string]string
}

var c = kvStoreServer{data: make(map[string]string)}

func (s *kvStoreServer) Get(ctx context.Context, request *pb.GetRequest) (*pb.GetResponse, error) {
	if value, ok := c.data[request.Key]; ok {
		return &pb.GetResponse{Value: value}, nil
	} else {
		return &pb.GetResponse{Value: ""}, errors.New("key not found")
	}
}
func (s *kvStoreServer) Set(ctx context.Context, request *pb.SetRequest) (*pb.SetResponse, error) {
	c.data[request.Key] = request.Value
	return &pb.SetResponse{Success: true}, nil
}
func (s *kvStoreServer) Delete(ctx context.Context, request *pb.DeleteRequest) (*pb.DeleteResponse, error) {
	if _, ok := c.data[request.Key]; ok {
		delete(c.data, request.Key)
		return &pb.DeleteResponse{Success: true}, nil
	} else {
		return &pb.DeleteResponse{Success: false}, nil
	}
}

var clientPool = make(map[int]pb.KvStoreClient)
var connPool = make(map[int]*grpc.ClientConn)

func connectAll() {
	for i := 0; i < 3; i++ {
		if i == id {
			continue
		}
		conn, err := grpc.Dial(fmt.Sprintf("server%v:50000", i), grpc.WithTransportCredentials(insecure.NewCredentials()))
		if err != nil {
			log.Fatalf("fail to dial: %v", err)
		}
		connPool[i] = conn
		client := pb.NewKvStoreClient(conn)
		clientPool[i] = client
	}
}
func closeAll() {
	for i := 0; i < 3; i++ {
		if err := connPool[i].Close(); err != nil {
			log.Printf("failed to close connection %v", err)
		}
	}
}

var id int

func main() {
	var err error
	id, err = strconv.Atoi(os.Args[1])
	if err != nil {
		log.Fatalf("failed to get id: %v", err)
	}
	//grpc server
	lis, err := net.Listen("tcp", "0.0.0.0:50000")
	if err != nil {
		log.Fatalf("failed to listen: %v", err)
	}
	grpcServer := grpc.NewServer()
	pb.RegisterKvStoreServer(grpcServer, &c)
	go func() {
		if err := grpcServer.Serve(lis); err != nil {
			log.Fatalf("failed to serve: %v", err)
		}
	}()
	//grpc client
	connectAll()
	defer closeAll()
	//http server
	log.Printf("start http server")
	r := mux.NewRouter()
	r.HandleFunc("/", set).Methods("POST")
	r.HandleFunc("/{key}", get).Methods("GET")
	r.HandleFunc("/{key}", deleteKey).Methods("DELETE")
	if err = http.ListenAndServe("0.0.0.0:8080", r); err != nil {
		fmt.Println(err)
	}
}
