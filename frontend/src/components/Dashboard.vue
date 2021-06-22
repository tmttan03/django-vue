<template>
  <div class="row">
    <h2>
      Agile Software Development
    </h2>
    <div class="col-md-6">
      <table class="table table-hover">
        <thead>
          <tr>
            <th scope="col">Value</th>
            <th scope="col">Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr
            v-for="(value, index) in values"
            :key="index"
          >
            <th scope="row">{{ value.name }}</th>
            <td>
              <button
                type="button"
                class="btn btn-secondary btn-sm m-2"
                @click="updateValue(value.id)"
              >Update</button>

              <button
                type="button"
                class="btn btn-danger btn-sm m-2"
                @click="deleteFeature(value.id)"
              >Delete</button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <div class="col-md-6">
      <table class="table table-hover">
        <thead>
          <tr>
            <th scope="col">Principle</th>
            <th scope="col">Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr
            v-for="(principle, index) in principles"
            :key="index"
          >
            <th scope="row">{{ principle.name }}</th>
            <td>
              <button
                type="button"
                class="btn btn-secondary btn-sm m-2"
                @click="updatePrinciple(principle.id)"
              >Update</button>

              <button
                type="button"
                class="btn btn-danger btn-sm m-2"
                @click="deleteFeature(principle.id)"
              >Delete</button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script>
import FeatureDataService from "../services/FeatureDataService";

export default {
  name: "dashboard",
  data() {
    return {
      values: [],
      principles: [],
      features: [],
      currentValues: null,
      currentPrinciples: null,
      currentIndex: -1,
      title: ""
    };
  },
  methods: {
    retrieveData() {
      FeatureDataService.getAll()
        .then(response => {
          this.features = response.data;
          this.values = this.features.filter(value => value.feat_type.includes('Values'));
          this.principles = this.features.filter(value => value.feat_type.includes('Principle'));
        })
        .catch(e => {
          console.log(e);
        });
    },

    refreshList() {
      this.retrieveData();
      this.currentFeature = null;
      this.currentValues = null;
      this.currentPrinciples = null;
      this.currentIndex = -1;
    },

    deleteFeature(id) {
      FeatureDataService.delete(id)
        .then(response => {
          console.log(response.data);
          this.features = this.features.filter(value => value.id !== id);
          this.values = this.features.filter(value => value.feat_type.includes('Values'));
          this.principles = this.features.filter(value => value.feat_type.includes('Principle'));
        })
        .catch(e => {
          console.log(e);
        });
    },

    updateValue(id){
      this.$router.push({ name: "value-details" , params: { id: id } });
    },

    updatePrinciple(id){
      this.$router.push({ name: "principle-details" , params: { id: id } });
    },

  },
  mounted() {
    this.retrieveData();
  }
};
</script>

<style>
.list {
  text-align: left;
  max-width: 750px;
  margin: auto;
}
</style>