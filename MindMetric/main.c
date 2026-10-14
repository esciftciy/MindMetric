#define _CRT_SECURE_NO_WARNINGS

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <windows.h>
#include <sqlext.h>
#include <shellapi.h>

#define CONNECTION_STRING "DRIVER={SQL Server};SERVER=localhost;DATABASE=MindMetricDB;Trusted_Connection=Yes;"

void log_to_ssms(const char* name, double kriz, double ask, double aile, double kariyer, double sosyal, double lieScore, int isValid, const char* archetype) {
    SQLHENV henv;
    SQLHDBC hdbc;
    SQLHSTMT hstmt;
    SQLRETURN retcode;

    SQLAllocHandle(SQL_HANDLE_ENV, SQL_NULL_HANDLE, &henv);
    SQLSetEnvAttr(henv, SQL_ATTR_ODBC_VERSION, (SQLPOINTER)SQL_OV_ODBC3, 0);
    SQLAllocHandle(SQL_HANDLE_DBC, henv, &hdbc);

    retcode = SQLDriverConnectA(hdbc, NULL, (SQLCHAR*)CONNECTION_STRING, SQL_NTS, NULL, 0, NULL, SQL_DRIVER_NOPROMPT);

    if (SQL_SUCCEEDED(retcode)) {
        printf("[SQL SERVER] SSMS Veritabanina Baglanti Basarili! 🟢\n");

        // 1. Katılımcıyı Ekle
        char q1[512];
        snprintf(q1, sizeof(q1), "INSERT INTO Participants (FullName) VALUES ('%s');", name);
        SQLAllocHandle(SQL_HANDLE_STMT, hdbc, &hstmt);
        SQLExecDirectA(hstmt, (SQLCHAR*)q1, SQL_NTS);
        SQLFreeHandle(SQL_HANDLE_STMT, hstmt);

        // 2. Test Sonucunu Ekle
        char q2[1024];
        snprintf(q2, sizeof(q2),
            "INSERT INTO TestResults (ParticipantID, KrizTheta, AskTheta, AileTheta, KariyerTheta, SosyalTheta, LieScaleScore, IsValidResult, DominantArchetype) "
            "VALUES ((SELECT TOP 1 ID FROM Participants ORDER BY ID DESC), %.2f, %.2f, %.2f, %.2f, %.2f, %.2f, %d, '%s');",
            kriz, ask, aile, kariyer, sosyal, lieScore, isValid, archetype);

        SQLAllocHandle(SQL_HANDLE_STMT, hdbc, &hstmt);
        retcode = SQLExecDirectA(hstmt, (SQLCHAR*)q2, SQL_NTS);
        if (SQL_SUCCEEDED(retcode)) {
            printf("[SQL SERVER] Kayit SSMS Veritabanina Eklendi -> Danisan: %s | Arketip: %s\n", name, archetype);
        }
        SQLFreeHandle(SQL_HANDLE_STMT, hstmt);
        SQLDisconnect(hdbc);
    }
    else {
        printf("[!] SQL Server Baglanti Hatasi! SSMS ve SQL Server servisinin acik oldugundan emin olun.\n");
    }

    SQLFreeHandle(SQL_HANDLE_DBC, hdbc);
    SQLFreeHandle(SQL_HANDLE_ENV, henv);
}

int main() {
    printf("==================================================\n");
    printf("   MINDMETRIC PRO - AKADEMIK PSİKOMETRI ENGINE     \n");
    printf("==================================================\n\n");

    char exePath[MAX_PATH];
    char htmlPath[MAX_PATH];

    GetModuleFileNameA(NULL, exePath, MAX_PATH);
    char* lastSlash = strrchr(exePath, '\\');
    if (lastSlash != NULL) *lastSlash = '\0';

    snprintf(htmlPath, sizeof(htmlPath), "%s\\index.html", exePath);

    printf("[+] Web Arayuzu Aciliyor: %s\n\n", htmlPath);

    HINSTANCE result = ShellExecuteA(NULL, "open", htmlPath, NULL, NULL, SW_SHOWNORMAL);
    if ((INT_PTR)result <= 32) {
        ShellExecuteA(NULL, "open", "index.html", NULL, NULL, SW_SHOWNORMAL);
    }

    printf("[SUCCESS] Sistem Aktif. Test sonuclari SSMS veritabanina kaydedilecek! 🚀\n");
    printf("--------------------------------------------------\n");
    printf("Cikmak icin ENTER'a basin...");

    getchar();
    return 0;
}