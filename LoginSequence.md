``` mermaid
sequenceDiagram
    participant Client as Client
    participant LoginController as LoginController
    participant LoginService as LoginService
    participant LoginDAO as LoginDAO
    participant LoginRepository as LoginRepository

    Note over Client,LoginController: User Login
    Client->>LoginController: POST /v1/login (LoginRequest)
    LoginController->>LoginService: loginUser(LoginRequest)
    LoginService->>LoginDAO: existsByEmailAndPassword(LoginRequest)
    LoginDAO->>LoginRepository: findByEmailAddressAndPassword(email, password)
    LoginRepository-->>LoginDAO: UserEntity/null
    alt UserEntity is null
        LoginDAO-->>LoginService: throws LoginException
        LoginService-->>LoginController: throws LoginException
        LoginController-->>Client: ResponseEntity (Error Response)
    else UserEntity found
        LoginDAO-->>LoginService: UserEntity
        LoginService-->>LoginController: LoginResponse (Success)
        LoginController-->>Client: ResponseEntity<LoginResponse> (Success)
    end

    Note over Client,LoginController: User Deletion
    Client->>LoginController: POST /v1/delete (DeleteRequest)
    LoginController->>LoginService: existsByEmail(emailAddress)
    LoginService->>LoginDAO: existsByEmail(emailAddress)
    LoginDAO->>LoginRepository: findByEmailAddress(emailAddress)
    LoginRepository-->>LoginDAO: UserEntity/null
    alt UserEntity is null
        LoginDAO-->>LoginService: true (User does not exist)
        LoginService-->>LoginController: ResponseEntity<DeleteResponse> (Error)
        LoginController-->>Client: ResponseEntity<DeleteResponse> (Error)
    else UserEntity found
        LoginService->>LoginDAO: deleteByEmailAddress(emailAddress)
        LoginDAO->>LoginRepository: deleteByEmailAddress(emailAddress)
        LoginRepository-->>LoginDAO: Integer (deletedRecords)
        alt deletedRecords == 0
            LoginDAO-->>LoginService: throws LoginException
            LoginService-->>LoginController: throws LoginException
            LoginController-->>Client: ResponseEntity (Error Response)
        else deletedRecords > 0
            LoginDAO-->>LoginService: Integer (deletedRecords)
            LoginService-->>LoginController: DeleteResponse (Success)
            LoginController-->>Client: ResponseEntity<DeleteResponse> (Success)
        end
    end
```
