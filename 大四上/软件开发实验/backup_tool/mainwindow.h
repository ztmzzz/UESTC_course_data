#ifndef MAINWINDOW_H
#define MAINWINDOW_H

#include <QMainWindow>

QT_BEGIN_NAMESPACE
namespace Ui { class MainWindow; }
QT_END_NAMESPACE

class MainWindow : public QMainWindow {
Q_OBJECT

public:
    MainWindow(QWidget *parent = nullptr);

    ~MainWindow();

private slots:

    void on_toolButton_clicked();

    void on_toolButton_2_clicked();

    void on_checkBox_stateChanged(int arg1);

    void on_backup_clicked();

    void on_restore_clicked();

    void on_verify_clicked();

private:
    Ui::MainWindow *ui;


};

#endif // MAINWINDOW_H
