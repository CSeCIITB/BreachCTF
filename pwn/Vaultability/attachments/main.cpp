#include <iostream>

using namespace std;

class Vault {
    char pin[16];

  public:
    virtual void enterPin() {
        cout << "Enter Vault PIN: ";
        cin >> pin;
    }
    virtual void showSecurityLog() { cout << &pin << endl; }
    virtual void triggerAlarm() { cout << "Security Breach Detected!" << endl; }
};

class BackupVault : public Vault {
    char pin[16];

  public:
    void enterPin() {
        cout << "Enter Backup Vault PIN: ";
        cin >> pin;
    }
};

void secretAccess() { system("cat flag.txt"); }

int menu(Vault *vault, Vault *backup) {
    cout << "1. Enter Vault PIN" << endl;
    cout << "2. View Security Log" << endl;
    cout << "3. Trigger Alarm" << endl;
    cout << "4. Enter Backup Vault PIN" << endl;
    cout << "5. View Backup Vault Log" << endl;
    cout << "6. Trigger Backup Vault Alarm" << endl;
    cout << "7. Exit" << endl;
    cout << "Enter your choice: ";

    int choice;
    cin >> choice;

    switch (choice) {
    case 1:
        vault->enterPin();
        break;
    case 2:
        vault->showSecurityLog();
        break;
    case 3:
        vault->triggerAlarm();
        break;
    case 4:
        backup->enterPin();
        break;
    case 5:
        backup->showSecurityLog();
        break;
    case 6:
        backup->triggerAlarm();
        break;
    case 7:
        return 1;
    default:
        cout << "Invalid choice" << endl;
        break;
    }
    return 0;
}

int main() {
    Vault vault;
    BackupVault backup;

    while (!menu(&vault, &backup))
        ;

    return 0;
}

