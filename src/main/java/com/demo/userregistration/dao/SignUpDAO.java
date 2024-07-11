package com.demo.userregistration.dao;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Component;

import com.demo.userregistration.exception.SignUpException;
import com.demo.userregistration.model.UserEntity;
import com.demo.userregistration.repository.SignUpRepository;

@Component
public class SignUpDAO {
	
    @Autowired
	private SignUpRepository signUpRepository;
	

	public UserEntity existsByEmail(String emailAddress) {
        return signUpRepository.findByEmailAddress(emailAddress);
    }

    public UserEntity saveUser(UserEntity signUpEntity) {
        try {
            return signUpRepository.save(signUpEntity);
        } catch (Exception e) {
            throw new SignUpException("Exception occurred while saving user", e);
        }
    }
	
	

}
