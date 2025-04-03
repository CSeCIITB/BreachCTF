#!/bin/bash
export TMPDIR=/tmp

echo "Compiling submission..."
# Compile the submission from /home/runner/submission.cpp instead of /submission.cpp
compile_output=$(g++ -O2 -std=c++17 /home/runner/submission.cpp -o /tmp/submission 2>&1)
compile_status=$?
if [ $compile_status -ne 0 ]; then
    echo "Compilation failed with status $compile_status:"
    echo "$compile_output"
    exit 1
fi
echo "Compilation succeeded."

# Ensure the compiled binary is executable.
chmod +x /tmp/submission

# Copy the binary into /home/runner so that it resides on an exec-enabled filesystem.
cp /tmp/submission /home/runner/submission_exec
chmod +x /home/runner/submission_exec

passed=0
total=0

# Create a copy of the testcases directory to enforce read-only behavior in the sandbox.
cp -r /testcases /tmp/testcases_copy
echo "Running test cases..."
for input_file in /tmp/testcases_copy/input*.txt; do
    # echo "Processing $input_file"
    total=$((total+1))
    test_index=$(basename "$input_file" | sed 's/input//;s/.txt//')
    expected_file="/tmp/testcases_copy/expect_output${test_index}.txt"
    # echo "here"
    if [ ! -f "$expected_file" ]; then
        echo "Missing expected output file for test case $test_index" >&2
        exit 1
    fi
    # echo "Input file: $input_file"
    # echo "Running test case $input_file"

    # Run the submission inside a bubblewrap sandbox.
    output=$(bwrap \
    --bind /home/runner/submission_exec /submission_exec \
    --ro-bind /tmp/testcases_copy /testcases \
    --tmpfs /tmp \
    --dev /dev \
    --proc /proc \
    --ro-bind /usr /usr \
    --ro-bind /bin /bin \
    --ro-bind /lib /lib \
    --ro-bind /lib64 /lib64 \
    --unshare-pid \
    --unshare-net \
    -- /submission_exec < "$input_file" 2>/dev/null)
    exit_status=$?
    echo "output = $output"
    if [ $exit_status -eq 124 ]; then
        echo "Test case $test_index timed out."
    elif [ $exit_status -ne 0 ]; then
        echo "Test case $test_index exited with non-zero status $exit_status."
    fi

    expected=$(cat "$expected_file")

    if [ "$output" = "$expected" ]; then
        echo "Test case $test_index passed."
        passed=$((passed+1))
    else
        echo "Test case $test_index failed."
        # echo "Output: $output"
    fi
done

echo "$passed out of $total test cases passed."

if [ "$passed" -eq "$total" ]; then
    echo "ALL TESTS PASSED"
else
    exit 1
fi
