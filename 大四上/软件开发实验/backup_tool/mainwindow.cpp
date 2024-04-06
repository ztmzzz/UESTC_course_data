#include "mainwindow.h"
#include "./ui_mainwindow.h"
#include <QFileDialog>
#include <QMessageBox>
#include "encrypt.h"
#include "compress.h"
#include "verify.h"

extern bool backup_file(const std::string &src, const std::string &dst);

extern std::string root_path;

extern bool restore_file(const std::string &path, const std::string &dst);


bool is_encrypt = false;

MainWindow::MainWindow(QWidget *parent)
        : QMainWindow(parent), ui(new Ui::MainWindow) {
    ui->setupUi(this);
}

MainWindow::~MainWindow() {
    delete ui;
}


void MainWindow::on_toolButton_clicked() {
    QString filePath = QFileDialog::getExistingDirectory(this, "请选择备份目录路径…", "./");
    ui->src_path->setText(filePath);
}


void MainWindow::on_toolButton_2_clicked() {
    QString filePath = QFileDialog::getExistingDirectory(this, "请选择文件保存路径…", "./");
    ui->dst_path->setText(filePath);
}


void MainWindow::on_checkBox_stateChanged(int arg1) {
    is_encrypt = ui->checkBox->isChecked();
}


void MainWindow::on_backup_clicked() {
    if (ui->dst_path->text().isEmpty() || ui->src_path->text().isEmpty()) {
        QMessageBox::warning(this, "警告", "请填写完整信息");
        return;
    }
    root_path = ui->src_path->text().toStdString();
    QDir dir(ui->dst_path->text());
    //打包为单文件
    if (!backup_file(ui->src_path->text().toStdString(), ui->dst_path->text().toStdString() + "/backup.tmp")) {
        QMessageBox::warning(this, "警告", "备份失败");
        return;
    }
    //压缩
    compress c;
    c.compress_file(ui->dst_path->text().toStdString() + "/backup.tmp", ui->dst_path->text().toStdString() + "/backup");
    dir.remove("backup.tmp");
    //加密
    if (is_encrypt) {
        if (ui->password->toPlainText().isEmpty()) {
            QMessageBox::warning(this, "警告", "请填写密码");
            return;
        }
        encrypt e(ui->password->toPlainText().toStdString());
        e.encrypt_file(ui->dst_path->text().toStdString() + "/backup",
                       ui->dst_path->text().toStdString() + "/backup.enc");
        dir.remove("backup");
    }
    QMessageBox::information(this, "备份完成", "备份完成");

}

void MainWindow::on_restore_clicked() {
    if (ui->dst_path->text().isEmpty() || ui->src_path->text().isEmpty()) {
        QMessageBox::warning(this, "警告", "请填写完整信息");
        return;
    }
    QDir dir(ui->dst_path->text());
    if (is_encrypt) {
        if (ui->password->toPlainText().isEmpty()) {
            QMessageBox::warning(this, "警告", "请填写密码");
            return;
        }
        encrypt e(ui->password->toPlainText().toStdString());
        e.encrypt_file(ui->dst_path->text().toStdString() + "/backup.enc",
                       ui->dst_path->text().toStdString() + "/backup");
        compress c;
        c.decompress_file(ui->dst_path->text().toStdString() + "/backup",
                          ui->dst_path->text().toStdString() + "/backup.tmp");
        dir.remove("backup");
        if (!restore_file(ui->dst_path->text().toStdString() + "/backup.tmp", ui->src_path->text().toStdString())) {
            QMessageBox::warning(this, "警告", "恢复失败");
            dir.remove("backup.tmp");
            return;
        }
        dir.remove("backup.tmp");
    } else {
        compress c;
        c.decompress_file(ui->dst_path->text().toStdString() + "/backup",
                          ui->dst_path->text().toStdString() + "/backup.tmp");
        if (!restore_file(ui->dst_path->text().toStdString() + "/backup.tmp", ui->src_path->text().toStdString())) {
            QMessageBox::warning(this, "警告", "恢复失败");
            dir.remove("backup.tmp");
            return;
        }
        dir.remove("backup.tmp");
    }
    QMessageBox::information(this, "恢复完成", "恢复完成");
}

void MainWindow::on_verify_clicked() {
    if (ui->dst_path->text().isEmpty() || ui->src_path->text().isEmpty()) {
        QMessageBox::warning(this, "警告", "请填写完整信息");
        return;
    }
    QDir dir(ui->dst_path->text());
    if (is_encrypt) {
        if (ui->password->toPlainText().isEmpty()) {
            QMessageBox::warning(this, "警告", "请填写密码");
            return;
        }
        encrypt e(ui->password->toPlainText().toStdString());
        e.encrypt_file(ui->dst_path->text().toStdString() + "/backup.enc",
                       ui->dst_path->text().toStdString() + "/backup");
        compress c;
        c.decompress_file(ui->dst_path->text().toStdString() + "/backup",
                          ui->dst_path->text().toStdString() + "/backup.tmp");
        if (verify(ui->src_path->text().toStdString(), ui->dst_path->text().toStdString() + "/backup.tmp")) {
            QMessageBox::information(this, "备份验证", "备份完好");
        } else {
            QMessageBox::warning(this, "备份验证", "备份损坏");
        }
        dir.remove("backup");
        dir.remove("backup.tmp");
    } else {
        compress c;
        c.decompress_file(ui->dst_path->text().toStdString() + "/backup",
                          ui->dst_path->text().toStdString() + "/backup.tmp");
        if (verify(ui->src_path->text().toStdString(), ui->dst_path->text().toStdString() + "/backup.tmp")) {
            QMessageBox::information(this, "备份验证", "备份完好");
        } else {
            QMessageBox::warning(this, "备份验证", "备份损坏");
        }
        dir.remove("backup.tmp");
    }
}

