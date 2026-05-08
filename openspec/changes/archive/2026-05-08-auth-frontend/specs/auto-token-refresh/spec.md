## ADDED Requirements

### Requirement: Interceptor catches 401 errors
The Axios response interceptor SHALL catch 401 Unauthorized errors.

#### Scenario: 401 received
- **WHEN** API returns 401 Unauthorized
- **THEN** the interceptor intercepts the error

### Requirement: Interceptor attempts token refresh on 401
The interceptor SHALL attempt to refresh the accessToken using the refreshToken on 401.

#### Scenario: Token refresh initiated
- **WHEN** 401 is received and refreshToken exists in authStore
- **THEN** the interceptor makes a POST request to /api/v1/auth/refresh with the refreshToken

### Requirement: Token refresh successful - retry original request
The interceptor SHALL retry the original request after successful token refresh.

#### Scenario: Refresh successful
- **WHEN** the refresh API returns new { accessToken, refreshToken }
- **AND** authStore is updated with new tokens
- **AND** the original request is retried with the new accessToken
- **AND** the response is returned to the caller

### Requirement: Token refresh failed - redirect to login
The interceptor SHALL redirect to login when token refresh fails.

#### Scenario: Refresh token expired or invalid
- **WHEN** the refresh API returns 401 or 400
- **AND** authStore.logout() is called
- **AND** the user is redirected to /login

### Requirement: Prevent multiple simultaneous refresh attempts
The interceptor SHALL prevent multiple refresh attempts for concurrent 401 errors.

#### Scenario: Multiple 401 responses
- **WHEN** multiple API requests receive 401 simultaneously
- **AND** only one refresh attempt is made
- **AND** all requests wait for the same refresh result

### Requirement: Clear tokens on refresh failure
The interceptor SHALL clear the authStore tokens when refresh fails.

#### Scenario: Refresh fails
- **WHEN** /api/v1/auth/refresh returns an error
- **AND** authStore.logout() is called
- **AND** accessToken and refreshToken are cleared from store