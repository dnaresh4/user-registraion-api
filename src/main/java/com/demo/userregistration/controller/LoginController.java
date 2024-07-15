package com.demo.userregistration.controller;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import com.demo.userregistration.exception.LoginException;
import com.demo.userregistration.service.LoginService;
import com.demo.userregistration.vo.DeleteRequest;
import com.demo.userregistration.vo.DeleteResponse;
import com.demo.userregistration.vo.LoginRequest;
import com.demo.userregistration.vo.LoginResponse;

@RestController
@RequestMapping("/v1")
public class LoginController {

    @Autowired
	private LoginService loginService;

	@PostMapping("/login")
    public ResponseEntity<LoginResponse> loginUser(@RequestBody LoginRequest loginRequest) {

        try {
            // Attempt to log in the user
            LoginResponse loginResponse = loginService.loginUser(loginRequest);

            if ("400".equals(loginResponse.getStatus())) {
                return ResponseEntity.badRequest().body(loginResponse);
            }

            return ResponseEntity.ok(loginResponse);

        } catch (LoginException le) {
            // Handle exception if any during user login
            throw new LoginException("Exception occurred while logging in the user");
        }
    }

	@PostMapping("/delete")
    public ResponseEntity<DeleteResponse> deleteUser(@RequestBody DeleteRequest deleteRequest) {

        // Check if email exists
        if (loginService.existsByEmail(deleteRequest.getEmailAddress())) {
            DeleteResponse deleteResponse = new DeleteResponse();
            deleteResponse.setStatus("400");
            deleteResponse.setMessage("EmailAddress does not exist");
            return ResponseEntity.badRequest().body(deleteResponse);
        }

        try {
            // Try to delete the user
            DeleteResponse deleteResponse = loginService.deleteUser(deleteRequest);
            return ResponseEntity.ok(deleteResponse);

        } catch (LoginException se) {
            // Handle exception if any during user deletion
            throw new LoginException("Exception occurred while deleting the user");
        }
    }

}
