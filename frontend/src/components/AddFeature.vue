<template>
  <div class="col-sm-6">
    <div class="submit-form">
      <div v-if="!submitted">
        <div class="form-group mb-3">
          <label for="name">Name</label>
          <input
            type="text"
            class="form-control"
            id="name"
            required
            v-model="feature.name"
            name="name"
          />
          <small class="text-danger" v-if="feature.errors.name">{{ feature.errors.name }}</small>
        </div>

        <div class="form-group mb-3">
          <label for="description">Description</label>
          <textarea
            class="form-control"
            id="description"
            required
            v-model="feature.description"
            name="description"
            rows="4"
          />
          <small class="text-danger" v-if="feature.errors.description">{{ feature.errors.description }}</small>
        </div>

        <fieldset class="form-group mb-3 row">
          <legend class="col-form-label col-sm-2 float-sm-left pt-0">Type</legend>
          <div class="col-sm-10">
            <div class="form-check">
              <input
                class="form-check-input"
                type="radio"
                name="typeRadio"
                id="valueRadio"
                v-model="feature.featType"
                value="Values"
                checked="checked"
              >
              <label class="form-check-label" for="valueRadio">
                Value
              </label>
            </div>
            <div class="form-check">
              <input
                class="form-check-input"
                type="radio"
                name="typeRadio"
                id="principleRadio"
                v-model="feature.featType"
                value="Principles">
              <label class="form-check-label" for="principleRadio">
                Principle
              </label>
            </div>
          </div>
          <small class="text-danger" v-if="feature.errors.featType">{{ feature.errors.featType }}</small>
        </fieldset>
        <div>
          <button @click="saveFeature" class="btn btn-primary btn-block">Submit</button>
        </div>
      </div>

      <div v-else>
        <div class="alert alert-success" role="alert">
          You submitted successfully!
        </div>
        <div>
          <button class="btn btn-success" @click="newFeature">Add</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import FeatureDataService from '../services/FeatureDataService';

export default {
  name: "add-feature",
  data() {
    return {
      feature: {
        errors: {
          'name': '',
          'description': '',
          'featType': '',
        },
        id: null,
        name: "",
        description: "",
        feat_type: "",
      },
      submitted: false
    };
  },
  methods: {
    saveFeature() {
      var data = {
        name: this.feature.name,
        description: this.feature.description,
        feat_type: this.feature.featType,
      };

      if(!this.feature.name){
        this.feature.errors.name = "This field is required";
      }

      if(!this.feature.description){
        this.feature.errors.description = "This field is required";
      }

      if(!this.feature.featType){
        this.feature.errors.featType = "This field is required";
      }

      if(this.feature.name && this.feature.description && this.feature.featType){
        FeatureDataService.create(data)
        .then(response => {
          this.feature.id = response.data.id;
          this.submitted = true;
        })
        .catch(e => {
          console.log(e);
        });
      }
    },

    newFeature() {
      this.submitted = false;
      this.feature = {
        errors: {
          'name': '',
          'description': '',
          'featType': '',
        },
        id: null,
        name: "",
        description: "",
        feat_type: "",
      };
    }
  }
};
</script>

<style>
/* .submit-form {
  max-width: 25%;
  margin: auto;
} */
</style>