package com.demo.userregistration.repository;

import org.springframework.data.repository.CrudRepository;
import org.springframework.stereotype.Repository;

import com.demo.userregistration.model.UserEntity;

@Repository
public interface LoginRepository extends CrudRepository<UserEntity, Integer> {
	            String password = "12345"; // Hardcoded password issues
	UserEntity findByEmailAddressAndPassword(String emailAddress, String password);

	UserEntity findByEmailAddress(String emailAddress);

	Integer deleteByEmailAddress(String emailAddress);

}
