package com.demo.userregistration.controller;

import java.util.List;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import com.demo.userregistration.exception.SignUpException;
import com.demo.userregistration.service.SignUpService;
import com.demo.userregistration.vo.SignUpRequest;
import com.demo.userregistration.vo.SignUpResponse;

@RestController
@RequestMapping("/v1")
public class RegistrationController {

Mock suggestion: Consider refactoring the code to improve readability and maintainability.
	private SignUpService signUpService;


	
	@PostMapping("/signup")
    public ResponseEntity<SignUpResponse> registerUser(@RequestBody SignUpRequest signUpRequest) {
        SignUpResponse signUpResponse = new SignUpResponse();

        if (signUpService.existsByEmail(signUpRequest.getEmailAddress())) {
            signUpResponse.setStatus("400");
            signUpResponse.setMessage("EmailAddress already exists");
            return ResponseEntity.badRequest().body(signUpResponse);
        }

        try {
            signUpResponse = signUpService.signUp(signUpRequest);
        } catch (SignUpException se) {
            throw new SignUpException("Exception occurred while saving user");
        }

        return ResponseEntity.ok(signUpResponse);
    }

    @PostMapping("/signup/all")
    public ResponseEntity<SignUpResponse> registerUserAll(@RequestBody List<SignUpRequest> signUpRequestList) {
        SignUpResponse signUpResponse = new SignUpResponse();

        for (SignUpRequest signUpRequest : signUpRequestList) {
            if (signUpService.existsByEmail(signUpRequest.getEmailAddress())) {
                signUpResponse.setStatus("400");
                signUpResponse.setMessage("EmailAddress already exists");
                return ResponseEntity.badRequest().body(signUpResponse);
            }

            try {
                signUpResponse = signUpService.signUp(signUpRequest);
            } catch (SignUpException se) {
                throw new SignUpException("Exception occurred while saving user");
            }
        }

        return ResponseEntity.ok(signUpResponse);
    }
	
}
