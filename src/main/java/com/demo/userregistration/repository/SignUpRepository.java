package com.demo.userregistration.repository;

import org.springframework.data.repository.CrudRepository;
import org.springframework.stereotype.Repository;

import com.demo.userregistration.model.UserEntity;

@Repository
public interface SignUpRepository extends CrudRepository<UserEntity, Integer> {
	
	UserEntity findByEmailAddress(String emailAddress);

}
