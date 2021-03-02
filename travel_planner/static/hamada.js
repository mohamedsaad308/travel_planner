const editModal = {
  emits: ["edit-user", "close"],
  props: ["user"],
  methods: {
    editUser() {
      this.$emit(
        "edit-user",
        this.$refs.userEmail.value,
        this.$refs.userFirstName.value,
        this.$refs.userLastName.value
      );
    },
    close() {
      this.$emit("close");
    },
  },
  template: "#edit-modal-template",
};
const deleteModal = {
  props: ["user"],
  template: "#delete-modal-template",
};
const createModal = {
  props: ["user"],
  template: "#create-modal-template",
};
