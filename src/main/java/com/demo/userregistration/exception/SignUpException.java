package com.demo.userregistration.exception;

public class SignUpException extends RuntimeException {

	/**
	 * 
	 */
	private static final long serialVersionUID = 1L;

	public SignUpException(String message, Throwable cause) {
		super(cause);
	}

	public SignUpException(String message) {
		super();
	}
	
	

}
