---
title: "README please"
date: 2025-03-28
layout: writeup
platform: pearlCTF 2025
categories: [pwn]
tags: [file descriptors, ghidra]
difficulty: Medium
---

# README please

## Challenge Description

We're given a binary along with some text files and a server to connect to.
Upon connection, it prompts us for a file name.
From the source, we can see that there's 3 files inside the `files` directory, flag.txt, default.txt, and note-1.txt.

## Decompiling the binary

I opened the binary in binary ninja and cleaned up the code a bit.
Here's the decompiled code:

```cpp
int32_t main(int32_t argc, char **argv, char **envp)
{
    void password;
    generate_password(&password, 0x7f);
    printf("Welcome to file reading service!");
    for (int32_t i = 0; i <= 1; i += 1){
        printf("\nEnter the file name: ");
        void filename;
        __isoc99_scanf("%s", &filename);
        char *rax_4 = __xpg_basename(&filename);
        FILE *fp = fopen(&filename, U"r");
        if (fp){
            int32_t isNotFlag = strcmp(rax_4, "flag.txt");
            void passwordInput;
            int32_t rax_8;

            if (!isNotFlag){
                printf("Enter password: ");
                __isoc99_scanf("%s", &passwordInput);
                rax_8 = strcmp(&passwordInput, &password);
            }

            if (isNotFlag || !rax_8){
                while (fgets(&passwordInput, 0x64, fp)){printf("%s", &passwordInput);}
                fclose(fp);
            }
            else{
                puts("Incorrect password!");
            }
        }
        else{
            puts("Please don't try anything funny!");
        }
    }
    return 0;
}
```

To summarize, it takes a file name as input and checks if the file exists.
If it does, it checks if the file is `flag.txt`.
If it is, it prompts for a password.
If the password is correct, it prints the contents of the file.
If the file is not `flag.txt`, it prints the contents of the file without asking for a password.
The password is generated using a `genearate_password` function. When I decompiled it, It didn't seem much useful to me It was just a random password generator.

## Initial Approach (buffer overflow)

I was thinking of using a buffer overflow to maybe overwrite the rax_4 or isNotFlag variable.
I tried to find the offset of the variables, but they were stored in registers.

## Vulnerability

I realised that we were given two attempts to read the file. That seemed oddly specific.
Also, the flag file is opened in read mode but only closed after entering in the correct password.
This means that the file descriptor is still open and we can use it to read the contents of the file.

## Finding the file descriptor

So I know that the file descriptor is somewhere inside `/proc`.
`/proc/{pid}/fd/3` to be precise. Finding out the pid took me a while.
In the end, I found out that the `/proc/stat` file contains the last pid of assigned.

## Solution

So I connected to the server and checked the `/proc/stat` file.
Say it was `1234`, then I would connect again and I knew that the file descriptor would be `/proc/1235/fd/3`.
So first I would read `files/flag.txt` and enter a wrong password. The file descriptor to the flag file would still be open.
Then I would read the `/proc/1235/fd/3` file and get the flag.

<!-- UPDATE I found a better solution -->

## UPDATE

While reading more about file descriptors, I found out that we didnt need to go through the hassle of finding the pid.
We could just use the `/proc/self/fd/3` file descriptor.
This would give us the file descriptor of the current process.
