<template>
  <div v-if="currentPrinciple" class="edit-form">
    <h4>{{ currentPrinciple.name }}</h4>

    <p>{{ message }}</p>

    <form>
      <div class="form-group mb-3">
        <label for="name">Name</label>
        <input type="text" class="form-control" id="name"
          v-model="currentPrinciple.name"
        />
      </div>
      <div class="form-group mb-3">
        <label for="description">Description</label>
        <textarea class="form-control" id="description"
          v-model="currentPrinciple.description"
        />
      </div>
    </form>

    <button type="submit" class="btn btn-secondary m-2"
      @click="updateValue"
    >
      Update
    </button>

    <button class="btn btn-danger m-2"
      @click="deleteValue"
    >
      Delete
    </button>

  </div>

  <div v-else>
    <br />
    <p>Please click on a value...</p>
  </div>
</template>

<script>
import FeatureDataService from '../services/FeatureDataService';

export default {
  name: "principle",
  data() {
    return {
      currentPrinciple: null,
      message: ''
    };
  },
  methods: {
    getValue(id) {
      FeatureDataService.get(id)
        .then(response => {
          this.currentPrinciple = response.data;
        })
        .catch(e => {
          console.log(e);
        });
    },

    updateValue() {
      FeatureDataService.update(this.currentPrinciple.id, this.currentPrinciple)
        .then(response => {
          console.log(response.data);
          this.message = 'This principle was updated successfully!';
        })
        .catch(e => {
          console.log(e);
        });
    },

    deleteValue() {
      FeatureDataService.delete(this.currentPrinciple.id)
        .then(response => {
          console.log(response.data);
          this.$router.push({ name: "dashboard" });
        })
        .catch(e => {
          console.log(e);
        });
    }
  },
  mounted() {
    this.message = '';
    this.getValue(this.$route.params.id);
  }
};
</script>

<style>
.edit-form {
  max-width: 300px;
  margin: auto;
}
</style>
