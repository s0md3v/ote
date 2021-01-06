<h4 align="center">OTE : One Time Email</h4>

<p align="center">
  <a href="https://github.com/s0md3v/ote/releases">
    <img src="https://img.shields.io/github/release/s0md3v/ote.svg">
  </a>
  <a href="https://github.com/s0md3v/ote/issues?q=is%3Aissue+is%3Aclosed">
      <img src="https://img.shields.io/github/issues-closed-raw/s0md3v/ote.svg">
  </a>
</p>

### Introduction
**ote** is a command line utility that generates temporary email address and automatically extracts OTPs or confirmation links from the incoming mails. It uses [1secmail.com](https://www.1secmail.com/api/)'s API to generate temporary emails.

It can be installed with pip as follows:

```
pip3 install ote
```

### Usage

Enter `ote` in your terminal, a random email address will be generated for you. Any OTP or confirmation link sent to this address will be printed on your terminal.

After that:
- If the link/OTP is not accurate, enter 'f' to print the link to the email to check it yourself.
- If you want to open the confirmation link in your browser right away, enter 'o' 
- To quit, either enter 'q' or press Ctrl+C

> Note: If your OTP or link was a false positive or was not detected at all, please create an issue with the email body attached. The more variations of OTPs we have, the better the detection will get over time.

#### Generate a custom email

`ote init myusername`

It will create an email of form `myusername@domain.com`. After this point, **ote** will use this personalized email every time.

#### Generate a secure email

`ote init`

It will generate a random 20 character email and save it for subsequent usage like the previous option.
