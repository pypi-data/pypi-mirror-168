# Summary

A package to help replace AWS credentials from the sso window. When you click
on an AWS credential, the text is copied to the clipboard. This package reads
the clipboard buffer and replaces the correct profile credentials in your
`~/.aws/credentials` file.

## Installation

`pip install rollcred`

## Usage

Goto to your AWS SSO login screen. Select the account and profile you would like to roll
credentials for, click on the link that says `command line or programmatic access`.
Under the section labeled **Option 2** click the box with the credentials. Clicking
the box will copy the contents to the clipboard.

Open a terminal window and type `rollcred`. The credential will be replaced in your
creds file. If the credential does not exist it will be appended to the end of the
file. If the file does not exist, it will be created at `~/.aws/credentials`
