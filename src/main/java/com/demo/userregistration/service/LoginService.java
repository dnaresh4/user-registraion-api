package com.demo.userregistration.service;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import com.demo.userregistration.dao.LoginDAO;
import com.demo.userregistration.exception.LoginException;
import com.demo.userregistration.model.UserEntity;
import com.demo.userregistration.vo.DeleteRequest;
import com.demo.userregistration.vo.DeleteResponse;
import com.demo.userregistration.vo.LoginRequest;
import com.demo.userregistration.vo.LoginResponse;

@Service
public class LoginService {
	
	@Autowired
	private LoginDAO loginDao;

	public LoginResponse loginUser(LoginRequest loginRequest) {
        LoginResponse loginResponse = new LoginResponse();
        UserEntity userEntity = loginDao.existsByEmailAndPassword(loginRequest);

        if (userEntity == null) {
            loginResponse.setStatus("400");
            loginResponse.setMessage("User login failed");
            throw new LoginException("Exception occurred while logging in the user");
        } else {
            loginResponse.setStatus("200");
            loginResponse.setMessage("User login successful");
        }

        return loginResponse;
    }

    public boolean existsByEmail(String emailAddress) {
        UserEntity userEntity = loginDao.existsByEmail(emailAddress);
        return userEntity == null;
    }

    public DeleteResponse deleteUser(DeleteRequest deleteRequest) {
        DeleteResponse deleteResponse = new DeleteResponse();
        int deletedRecords = loginDao.deleteByEmailAddress(deleteRequest.getEmailAddress());

        if (deletedRecords == 0) {
            throw new LoginException("Exception occurred while deleting the user");
        }

        deleteResponse.setStatus("200");
        deleteResponse.setMessage("User information deleted successfully");
        return deleteResponse;
    }

}
