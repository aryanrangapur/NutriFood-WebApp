# Security Policy

## Supported Versions

The following versions of the project are currently being supported with security updates:

| Version | Supported          |
| ------- | ------------------ |
| 1.0.0   | :white_check_mark:  |
| < 1.0.0 | :x:                |

## Reporting a Vulnerability

We take security issues seriously. If you discover any security vulnerability, please follow the guidelines below to report it.

### Steps to report

1. **Email the Team:** If you believe you've found a security vulnerability, please notify us by sending an email to [aryan.rangapur717@gmail.com]. Include the following information:
   - A description of the issue
   - Steps to reproduce the vulnerability
   - Any supporting screenshots or code snippets

2. **Do Not Publicly Disclose:** Please do not publicly disclose the issue until we have had a chance to investigate and resolve it.

3. **Fix Timeline:** We will confirm the vulnerability and provide an initial response within 72 hours. A fix will be made within 14 business days depending on the severity.

## Security Considerations

- **Password Management:** We utilize the `Werkzeug.security` package for hashing and checking passwords using `generate_password_hash` and `check_password_hash`. Ensure that sensitive data, like user passwords, are hashed before being stored in MongoDB.
- **MongoDB Configuration:** MongoDB connections are configured using a MongoDB URI. We recommend storing your MongoDB URI and credentials securely, such as in environment variables (`os.environ`), to avoid exposing them in the codebase. 
- **API Key Exposure:** The Edamam API credentials (`EDAMAM_API_ID`, `EDAMAM_API_KEY`) are stored in the code, which can be a security concern. We strongly recommend using environment variables or secret managers to secure sensitive API keys and credentials.
- **File Upload Security:** The application allows users to upload images, but the allowed file extensions are restricted to prevent the upload of malicious files. Supported file types include `.png`, `.jpg`, `.jpeg`, and `.gif`.
- **Prediction Logic:** Input images are pre-processed before being passed to the TensorFlow model, and the file type is validated. Make sure all incoming data is sanitized properly to prevent malicious code execution.
- **SSL/TLS:** It is recommended to run the Flask application with SSL/TLS encryption, especially when handling sensitive information like login credentials.
- **Session Management:** Ensure that user sessions are managed securely, with proper session timeouts and secure cookie flags set.

## Dependencies

The application uses the following dependencies, which should be regularly updated to avoid security vulnerabilities:

- Flask (`v2.2.5`)
- pymongo (`v4.5.0`)
- Werkzeug (`v2.2.3`)
- TensorFlow (`v2.13.0`)
- NumPy (`v1.24.2`)
- Pillow (`v9.4.0`)
- Requests (`v2.31.0`)
- Gunicorn (`v21.0.1`)

### Updating Dependencies

Regularly check for updates and apply them using:

   ```bash
      pip install --upgrade <package_name>
 ```


This ensures that you are using the latest, most secure versions of your dependencies.
