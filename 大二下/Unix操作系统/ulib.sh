#!/bin/bash
# 一个脚本化的图书馆系统
#
BOLD=$(tput smso)   # 粗体字体
NORMAL=$(tput rmso) # 正常字体
export BOLD NORMAL

greeting() {
    tput clear
    tput cup 7 25
    printf "${BOLD}Super Duper Unix Library"
    tput cup 15 15
    printf "${NORMAL}This is the Unix library application"
    tput cup 17 15
    printf "Please enter any key to continue...\n"
}

handle_error() {
    # 显示错误信息
    tput cup $1 $2
    printf "Wrong input, try again\n"
    tput cup $(($1+1)) $2
    printf "Press any key to continue...> "
    read ANSWER
    # 清掉错误显示
    tput cup $1 $2
    tput ed
}

editmenu() {
    while true; do
        # 显示编辑菜单
        tput clear
        tput cup 5 10
        printf "Unix Library - ${BOLD}EDIT MENU${NORMAL}"
        tput cup 7 20
        printf "0: ${BOLD}RETURN${NORMAL} to main menu"
        tput cup 9 20
        printf "1: ${BOLD}ADD${NORMAL}"
        tput cup 11 20
        printf "2: ${BOLD}UPDATE${NORMAL}"
        tput cup 13 20
        printf "3: ${BOLD}DISPLAY${NORMAL}"
        tput cup 15 20
        printf "4: ${BOLD}DELETE${NORMAL}"

        # 处理编辑菜单
        tput cup 17 10
        printf "Enter your choice > "
        read CHOICE
        case "$CHOICE" in
            0) return;;
            1) add_book;;
            2) update_book;;
            3) display_book;;
            4) delete_book;;
            *) handle_error 20 10;;
        esac
    done
}

add_book() {
	tput clear
	tput cup 5 10
        printf "Unix Library - ${BOLD}ADD MODE${NORMAL}"
	tput cup 10 15
	printf "Title:		"
	read TITLE
	tput cup 12 15
	printf "Author:		"
	read AUTHOR
	tput cup 14 15
	printf "Category:	"
	tput cup 16 15
	printf "sys: system, ref: reference, tb: textbook"
	tput cup 14 32
	read CATEGORY
	case "$CATEGORY" in
		sys) CATEGORY=system;;
		ref) CATEGORY=reference;;
		tb) CATEGORY=textbook;;
	esac
	echo "$TITLE:$AUTHOR:$CATEGORY:in::" >> ULIB_FILE
	tput cup 18 10
	printf "Any more to add? (Y)es or (N)o >"
	read CHOICE
	case "$CHOICE" in
		Y|y|yes|Yes) add_book;;
		*) return;;
	esac
}
delete_book() {
	tput clear
	tput cup 2 5
	printf "Enter the author/title>"
	read AT
	grep -i "$AT" ULIB_FILE > temp
	if [ -s temp ];then
		OLDIFS="$IFS"
		IFS=":"
		read TITLE AUTHOR CATEGORY STATUS BNAME DATE < temp
		IFS="$OLDIFS"
		tput cup 5 10
        	printf "Unix Library - ${BOLD}DELETE MODE${NORMAL}"
		tput cup 10 15
		printf "Title:		$TITLE"
		tput cup 12 15
		printf "Author:		$AUTHOR"
		tput cup 14 15
		printf "Category:	$CATEGORY"
		tput cup 16 15
		printf "Status:		$STATUS"
		if [ "$STATUS" = "out" ];then
			tput cup 18 15
			printf "Checked out by:	$BNAME"
			tput cup 20 15
			printf "Date:		$DATE"
		fi
	else
		tput cup 4 5
		printf "$AT not found"
	fi
	tput cup 26 15
	printf "Delete this book? (Y)es or (N )o >"
	read CHOICE
	case "$CHOICE" in
		Y|y|yes|Yes) grep -v "$TITLE:$AUTHOR:$CATEGORY:$STATUS:$BNAME:$DATE" ULIB_FILE > temp;mv temp ULIB_FILE;;
		*) return;;
	esac
	tput cup 28 10
	printf "Any more to delete? (Y)es or (N)o >"
	read CHOICE
	case "$CHOICE" in
		Y|y|yes|Yes) delete_book;;
		*) return;;
	esac
}
display_book(){
	tput clear
	tput cup 2 5
	printf "Enter the author/title>"
	read AT
	grep -i "$AT" ULIB_FILE > temp
	if [ -s temp ];then
		OLDIFS="$IFS"
		IFS=":"
		read TITLE AUTHOR CATEGORY STATUS BNAME DATE < temp
		IFS="$OLDIFS"
		tput cup 5 10
	    	printf "Unix Library - ${BOLD}DISPLAY MODE${NORMAL}"
		tput cup 10 15
		printf "Title:		$TITLE"
		tput cup 12 15
		printf "Author:		$AUTHOR"
		tput cup 14 15
		printf "Category:	$CATEGORY"
		tput cup 16 15
		printf "Status:		$STATUS"
		if [ "$STATUS" = "out" ];then
			tput cup 18 15
			printf "Checked out by:	$BNAME"
			tput cup 20 15
			printf "Date:		$DATE"
		fi
	else
		tput cup 4 5
		printf "$AT not found"
	fi
	tput cup 28 10
	printf "Any more to look for? (Y)es or (N)o >"
	read CHOICE
	case "$CHOICE" in
		Y|y|yes|Yes) display_book;;
		*) return;;
	esac
}
update_book(){
	tput clear
	tput cup 2 5
	printf "Enter the author/title>"
	read AT
	grep -i "$AT" ULIB_FILE > temp
	if [ -s temp ];then
		OLDIFS="$IFS"
		IFS=":"
		read TITLE AUTHOR CATEGORY STATUS BNAME DATE < temp
		IFS="$OLDIFS"
		tput cup 5 10
	    	printf "Unix Library - ${BOLD}UPDATE STATUS MODE${NORMAL}"
		tput cup 10 15
		printf "Title:		$TITLE"
		tput cup 12 15
		printf "Author:		$AUTHOR"
		tput cup 14 15
		printf "Category:	$CATEGORY"
		tput cup 16 15
		printf "Status:		$STATUS"
		if [ "$STATUS" = "in" ];then
			NSTATUS=out
			tput cup 18 15
			printf "New Status:	$NSTATUS"
			tput cup 20 15
			printf "Checked out by:	"
			read NBNAME
			tput cup 22 15
			NDATE=$(date +%D)
			printf "Date:		$NDATE"
		else
			NSTATUS=in
			tput cup 18 15
			printf "Checked out by:	$BNAME"
			tput cup 20 15
			printf "Date:		$DATE"
			tput cup 22 15
			printf "New Status:	$NSTATUS"
		fi
		grep -v "$TITLE:$AUTHOR:$CATEGORY:$STATUS:$BNAME:$DATE" ULIB_FILE > temp
		mv temp ULIB_FILE
		echo "$TITLE:$AUTHOR:$CATEGORY:$NSTATUS:$NBNAME:$NDATE" >> ULIB_FILE
	else
		tput cup 4 5
		printf "$AT not found"
	fi
	tput cup 28 10
	printf "Any more to update? (Y)es or (N)o >"
	read CHOICE
	case "$CHOICE" in
		Y|y|yes|Yes) update_book;;
		*) return;;
	esac
}
mainmenu() {
    # 显示菜单
    tput clear
    tput cup 5 10
    printf "Unix Library - ${BOLD}Main menu${NORMAL}\n"
    tput cup 7 20
    printf "0: ${BOLD}EXIT${NORMAL} this program\n"
    tput cup 9 20
    printf "1: ${BOLD}EDIT${NORMAL} menu\n"
    tput cup 11 20
    printf "2: ${BOLD}REPORTS${NORMAL} menu\n"

    # 处理分支
    tput cup 13 10
    printf "Enter your choice > "
    read CHOICE
    case "$CHOICE" in
        0) tput clear; exit 0;;
        1) editmenu;;
        2) reportmenu;;      #reportmenu;;
        *) handle_error 20 10
    esac
}

reportmenu(){
while true;
do
	tput clear
    tput cup 5 10
    printf "Unix Library - ${BOLD}REPORTS MENU${NORMAL}\n"
    tput cup 7 20
    printf "0: ${BOLD}RETURN${NORMAL}\n"
    tput cup 9 20
    printf "1: Sorted by ${BOLD}TITLES${NORMAL}\n"
    tput cup 11 20
    printf "2: Sorted by ${BOLD}AUTHOR${NORMAL}\n"
    tput cup 13 20
    printf "3: Sorted by ${BOLD}CATEGORY${NORMAL}\n"

    # 处理分支
    tput cup 15 10
    printf "Enter your choice > "
    read CHOICE
    case "$CHOICE" in
        0) return;;
        1) sort -f -d -t : ULIB_FILE > temp;report;;
        2) sort -f -d -t : +1 ULIB_FILE > temp;report;;
        3) sort -f -d -t : +2 ULIB_FILE > temp;report;;
        *) handle_error 20 10
    esac
done
}
report(){
	OLDIFS="$IFS"
	IFS=":"
	while read TITLE AUTHOR CATEGORY STATUS BNAME DATE
	do
		printf "Title:		$TITLE\n" >> ttemp
		printf "Author:		$AUTHOR\n" >> ttemp
		printf "Category:	$CATEGORY\n" >> ttemp
		printf "Status:		$STATUS\n" >> ttemp
		if [ "$STATUS" = "out" ];then
			printf "Checked out by:	$BNAME\n" >> ttemp
			printf "Date:		$DATE\n" >> ttemp
		fi
	done < temp
	IFS="$OLDIFS"
	more -d -c ttemp
	read A
	rm temp ttemp
}
# 欢迎界面
greeting

# 处理循环
read ANSWER
while true; do
    mainmenu
done


