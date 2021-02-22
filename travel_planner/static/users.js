//startign with view
// register modal component

const editModal = {
  props: ["user"],
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
const app = new Vue({
  el: "#app",
  components: {
    "edit-modal": editModal,
    "delete-modal": deleteModal,
    "create-modal": createModal,
  },
  delimiters: ["${", "}"],
  data: {
    showEditModal: false,
    showDeleteModal: false,
    showCreateModal: false,
    users: [],
    error: "",
    search: "",
    isActive: true,
    hasError: false,
    userToEdit: {},
    userToDelete: {},
    userToCreat: {},
  },
  created() {
    fetch("/api/users", {
      method: "GET",
      credentials: "include",
      cache: "no-cache",
      headers: new Headers({
        "content-type": "application/json",
      }),
    })
      .then((response) => response.json())
      .then((json) => {
        console.log(json.users);
        this.users = json.users;
      });
  },
  methods: {
    getToEditUser(toEditID) {
      // const userID = el.id.split("-")[1];
      this.showEditModal = true;
      console.log(toEditID);
      this.userToEdit = this.users.find((obj) => obj.id == toEditID);
      console.log(this.userToEdit);
    },
    getToDeleteUser(id) {
      // const userID = el.id.split("-")[1];
      this.showDeleteModal = true;
      console.log(id);
      this.userToDelete = this.users.find((obj) => obj.id == id);
      console.log(this.userToDelete);
    },
    updateUser() {
      fetch(`/api/users/${this.userToEdit.id}`, {
        method: "PATCH",
        credentials: "include",
        cache: "no-cache",
        body: JSON.stringify({
          email: this.userToEdit.email,
          first_name: this.userToEdit.first_name,
          last_name: this.userToEdit.last_name,
        }),
        headers: new Headers({
          "content-type": "application/json",
        }),
      })
        .then((response) => response.json())
        .then((json) => {
          console.log(json);
          if (json.success) {
            this.userToEdit.email = json.user.email;
            this.userToEdit.first_name = json.user.first_name;
            this.userToEdit.last_name = json.user.last_name;
            this.showEditModal = false;
            this.error = "";
          } else {
            this.error = json.error;
          }
        });
    },
    deleteUser() {
      fetch(`/api/users/${this.userToDelete.id}`, {
        method: "DELETE",
        credentials: "include",
        cache: "no-cache",
        headers: new Headers({
          "content-type": "application/json",
        }),
      })
        .then((response) => response.json())
        .then((json) => {
          console.log(json);
          if (json.success) {
            this.users = this.users.filter((user) => user.id != json.user_id);
            console.log("users updated");
            this.showDeleteModal = false;
            this.error = "";
          } else {
            this.error = json.error;
          }
        });
    },
    searchUsers() {
      this.search = this.$refs.userSearch.value;
      console.log("search", this.search);
      fetch("/api/users/search", {
        method: "POST",
        credentials: "include",
        cache: "no-cache",
        body: JSON.stringify({
          search: this.search,
        }),
        headers: new Headers({
          "content-type": "application/json",
        }),
      })
        .then((response) => response.json())
        .then((json) => {
          console.log(json);
          if (json.success) {
            this.users = json.users;
            this.$refs.userSearch.value = "";
            console.log("users searched");
          }
        });
    },
    createUser() {},
  },
});
