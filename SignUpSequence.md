``` mermaid
sequenceDiagram
    participant Client as Client
    participant RegistrationController as RegistrationController
    participant SignUpService as SignUpService
    participant SignUpDAO as SignUpDAO
    participant SignUpRepository as SignUpRepository

    Note over Client,RegistrationController: User Registration Single
    Client->>RegistrationController: POST /signup (SignUpRequest)
    RegistrationController->>SignUpService: existsByEmail(emailAddress)
    SignUpService->>SignUpDAO: existsByEmail(emailAddress)
    SignUpDAO->>SignUpRepository: findByEmailAddress(emailAddress)
    SignUpRepository-->>SignUpDAO: UserEntity/null
    SignUpDAO-->>SignUpService: true/false
    alt Email does not exist
        SignUpService->>SignUpDAO: saveUser(UserEntity)
        SignUpDAO->>SignUpRepository: save(UserEntity)
        SignUpRepository-->>SignUpDAO: UserEntity
        SignUpDAO-->>SignUpService: UserEntity
        SignUpService-->>RegistrationController: SignUpResponse (Success)
    else Email exists
        RegistrationController-->>Client: ResponseEntity<SignUpResponse> (Email exists)
    end

    Note over Client,RegistrationController: User Registration Bulk
    Client->>RegistrationController: POST /signup/all (List<SignUpRequest>)
    loop for each SignUpRequest
        RegistrationController->>SignUpService: existsByEmail(emailAddress)
        SignUpService->>SignUpDAO: existsByEmail(emailAddress)
        SignUpDAO->>SignUpRepository: findByEmailAddress(emailAddress)
        SignUpRepository-->>SignUpDAO: UserEntity/null
        SignUpDAO-->>SignUpService: true/false
        alt Email does not exist
            SignUpService->>SignUpDAO: saveUser(UserEntity)
            SignUpDAO->>SignUpRepository: save(UserEntity)
            SignUpRepository-->>SignUpDAO: UserEntity
            SignUpDAO-->>SignUpService: UserEntity
            SignUpService-->>RegistrationController: SignUpResponse (Success)
        else Email exists
            RegistrationController-->>Client: ResponseEntity<SignUpResponse> (Email exists)
        end
    end
```
