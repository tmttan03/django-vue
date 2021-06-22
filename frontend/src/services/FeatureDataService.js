import http from "../http-common";

class FeatureDataService {

  getAll() {
    return http.get("/features/");
  }

  getValues(){
    return http.get("/features/values/");
  }

  getPrinciples(){
    return http.get("/features/principles/");
  }

  get(id) {
    return http.get(`/features/?id=${id}`);
  }

  create(data) {
    return http.post("/features/add/", data);
  }

  update(id, data) {
    return http.put(`/features/update/?id=${id}`, data);
  }

  delete(id) {
    return http.delete(`/features/delete/?id=${id}`);
  }
}

export default new FeatureDataService();