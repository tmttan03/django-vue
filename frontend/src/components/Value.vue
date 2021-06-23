<template>
  <div v-if="currentValue" class="edit-form">
    <h4>Edit</h4>

    <p>{{ message }}</p>

    <form>
      <div class="form-group mb-3">
        <label for="name">Name</label>
        <input type="text" class="form-control" id="name"
          v-model="currentValue.name"
        />
      </div>
      <div class="form-group mb-3">
        <label for="description">Description</label>
        <textarea class="form-control" id="description"
          v-model="currentValue.description"
          rows="4"
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
  name: "value",
  data() {
    return {
      currentValue: null,
      message: ''
    };
  },
  methods: {
    getValue(id) {
      FeatureDataService.get(id)
        .then(response => {
          this.currentValue = response.data;
          console.log(response.data);
        })
        .catch(e => {
          console.log(e);
        });
    },

    updateValue() {
      FeatureDataService.update(this.currentValue.id, this.currentValue)
        .then(response => {
          console.log(response.data);
          this.message = 'This value was updated successfully!';
        })
        .catch(e => {
          console.log(e);
        });
    },

    deleteValue() {
      FeatureDataService.delete(this.currentValue.id)
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
  max-width: 500px;
  margin: auto;
}
</style>
