import httpClient from './httpClient';

const END_POINT = '/rest-auth/registration';

// get list of registration requests to approve
const getRegistrationRequests = () => httpClient.get(`${END_POINT}/`);

export {
    getRegistrationRequests
}