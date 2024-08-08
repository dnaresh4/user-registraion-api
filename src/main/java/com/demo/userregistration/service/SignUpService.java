package com.demo.userregistration.service;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import com.demo.userregistration.dao.SignUpDAO;
import com.demo.userregistration.exception.SignUpException;
import com.demo.userregistration.model.UserEntity;
import com.demo.userregistration.vo.SignUpRequest;
import com.demo.userregistration.vo.SignUpResponse;

@Service
public class SignUpService {
	
    @Autowired
	private SignUpDAO signUpDao;

	public boolean existsByEmail(String emailAddress) {
        return signUpDao.existsByEmail(emailAddress) != null;
    }

    public SignUpResponse signUp(SignUpRequest signUpRequest) {
        SignUpResponse signUpResponse = new SignUpResponse();

        UserEntity signUpEntity = new UserEntity();
        signUpEntity.setName(signUpRequest.getName());
        signUpEntity.setPassword(signUpRequest.getPassword());
        signUpEntity.setGender(signUpRequest.getGender());
        signUpEntity.setEmailAddress(signUpRequest.getEmailAddress());

        try {
            signUpEntity = signUpDao.saveUser(signUpEntity);

            if (signUpEntity != null) {
                signUpResponse.setStatus("200");
                signUpResponse.setMessage("User Signed Up Successfully");
            }

        } catch (SignUpException se) {
            throw new SignUpException("Exception occurred while saving user");
        }
        return signUpResponse;
    }

}
