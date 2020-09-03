import httpClient from './httpClient';

const END_POINT = '/rest-auth';

// used to validate tokens received from social login
const convertToken = (params) => httpClient.post(`${END_POINT}/user/`, params);

// used to refresh current access token
const getNewToken = (params) => httpClient.post(`${END_POINT}/user/`, params);

export {
    convertToken,
    getNewToken
}