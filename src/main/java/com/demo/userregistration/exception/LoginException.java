package com.demo.userregistration.exception;

public class LoginException extends RuntimeException {

	/**
	 * 
	 */
	private static final long serialVersionUID = 1L;

	public LoginException(String message, Throwable cause) {
		super(cause);
	}

	public LoginException(String message) {
		super();
	}
	
	

}
