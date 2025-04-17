#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

int main() {
    // Execute the submission runner script.
    execl("/bin/bash", "bash", "/run_submission.sh", (char *)NULL);
    perror("execl");
    return 1;
}
