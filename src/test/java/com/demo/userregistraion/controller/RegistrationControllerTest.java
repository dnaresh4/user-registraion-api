package com.demo.userregistraion.controller;
import static org.junit.Assert.assertEquals;
import static org.mockito.Mockito.*;

import org.junit.Before;
import org.junit.Test;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.MockitoAnnotations;
import org.springframework.http.ResponseEntity;

import com.demo.userregistration.controller.RegistrationController;
import com.demo.userregistration.exception.SignUpException;
import com.demo.userregistration.service.SignUpService;
import com.demo.userregistration.vo.SignUpRequest;
import com.demo.userregistration.vo.SignUpResponse;

public class RegistrationControllerTest {

 @Mock
 private SignUpService signUpService;

 @InjectMocks
 private RegistrationController registrationController;

 @Before
 public void setup() {
MockitoAnnotations.openMocks(this);
 }

 @Test
 public void testRegisterUser_Success() {
 SignUpRequest signUpRequest = new SignUpRequest();
 signUpRequest.setEmailAddress("test@example.com");

 SignUpResponse expectedResponse = new SignUpResponse();
 expectedResponse.setStatus("200");
 expectedResponse.setMessage("User registered successfully");

 when(signUpService.existsByEmail(signUpRequest.getEmailAddress())).thenReturn(false);
 when(signUpService.signUp(signUpRequest)).thenReturn(expectedResponse);

 ResponseEntity<SignUpResponse> responseEntity = registrationController.registerUser(signUpRequest);
 SignUpResponse actualResponse = responseEntity.getBody();

 assertEquals(200, responseEntity.getStatusCodeValue());
 assertEquals(expectedResponse, actualResponse);
 }

 @Test
 public void testRegisterUser_EmailExists() {
 SignUpRequest signUpRequest = new SignUpRequest();
 signUpRequest.setEmailAddress("test@example.com");

 SignUpResponse expectedResponse = new SignUpResponse();
 expectedResponse.setStatus("400");
 expectedResponse.setMessage("EmailAddress already exists");

 when(signUpService.existsByEmail(signUpRequest.getEmailAddress())).thenReturn(true);

 ResponseEntity<SignUpResponse> responseEntity = registrationController.registerUser(signUpRequest);
 SignUpResponse actualResponse = responseEntity.getBody();

 assertEquals(400, responseEntity.getStatusCode().value());
 }

 @Test(expected = SignUpException.class)
 public void testRegisterUser_Exception() {
 SignUpRequest signUpRequest = new SignUpRequest();
 signUpRequest.setEmailAddress("test@example.com");

 when(signUpService.existsByEmail(signUpRequest.getEmailAddress())).thenReturn(false);
 when(signUpService.signUp(signUpRequest)).thenThrow(new SignUpException("Exception occurred while saving user"));

 registrationController.registerUser(signUpRequest);
 }
}
