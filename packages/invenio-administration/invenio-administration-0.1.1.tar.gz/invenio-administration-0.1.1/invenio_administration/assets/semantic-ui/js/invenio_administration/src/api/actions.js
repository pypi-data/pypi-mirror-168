import { APIRoutes } from "./routes";
import { http } from "./config";

const getResource = async (apiEndpoint, pid) => {
  return await http.get(APIRoutes.get(apiEndpoint, pid));
};

const deleteResource = async (resource, apiEndpoint, idKeyPath = "pid") => {
  return await http.delete(APIRoutes.detailsView(apiEndpoint, resource, idKeyPath));
};

const editResource = async (apiEndpoint, pid, payload) => {
  return await http.put(APIRoutes.get(apiEndpoint, pid), payload);
};

const createResource = async (apiEndpoint, payload) => {
  return await http.post(apiEndpoint, payload);
};

const resourceAction = async (endpoint, payload) => {
  return await http.post(endpoint, payload);
};

export const InvenioAdministrationActionsApi = {
  deleteResource: deleteResource,
  editResource: editResource,
  getResource: getResource,
  resourceAction: resourceAction,
  createResource: createResource,
};
