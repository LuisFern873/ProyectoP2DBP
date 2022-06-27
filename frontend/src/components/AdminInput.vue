<template>
  <label>
    {{ label }}
    <input :type="type" v-model="inputValue" />
  </label>
</template>

<script>
export default {
  name: "admin-input",
  props: ["label", "type", "modelValue"],
  computed: {
    inputValue: {
      get() {
        return this.modelValue;
      },
      set(value) {
        this.$emit("update:modelValue", value);
      },
    },
  },
};
</script>
