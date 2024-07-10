package com.demo.userregistration.dao;

import jakarta.transaction.Transactional;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Component;

import com.demo.userregistration.exception.LoginException;
import com.demo.userregistration.model.UserEntity;
import com.demo.userregistration.repository.LoginRepository;
import com.demo.userregistration.vo.LoginRequest;

@Component
public class LoginDAO {
	
	@Autowired
	private LoginRepository loginRepository;
	

	public UserEntity existsByEmailAndPassword(LoginRequest loginRequest) {
		UserEntity user =  loginRepository.findByEmailAddressAndPassword(loginRequest.getEmailAddress(), loginRequest.getPassword());
		if(user == null) {
    		throw new LoginException("User with email address and password doesnot exists");
    	}
        return user;
    }

    public UserEntity existsByEmail(String emailAddress) {
    	
        return loginRepository.findByEmailAddress(emailAddress);
    }

    @Transactional
    public Integer deleteByEmailAddress(String emailAddress) {
        Integer deletedRecords = loginRepository.deleteByEmailAddress(emailAddress);

        if (deletedRecords == 0) {
            throw new LoginException("User with email address " + emailAddress + " not found for deletion");
        }

        return deletedRecords;
    }

}
