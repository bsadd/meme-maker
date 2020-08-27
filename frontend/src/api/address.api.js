import httpClient from './httpClient';

const END_POINT = '/coreapp/address';

// used to fetch any address resource
const getAddressById = (uuid) => httpClient.get(`${END_POINT}/${uuid}/`);

// used to create new address resource
const createAddress = (address) => httpClient.post(`${END_POINT}/`, address);

// used to update any address resource
const updateAddress = (uuid, address) => httpClient.patch(`${END_POINT}/${uuid}/`, address);

export {
    getAddressById,
    createAddress,
    updateAddress
}