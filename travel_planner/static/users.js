//startign with view
// register modal component

// const editModal = {
//   props: ["user"],
//   template: "#edit-modal-template",
// };
// const deleteModal = {
//   props: ["user"],
//   template: "#delete-modal-template",
// };
// const createModal = {
//   props: ["user"],
//   template: "#create-modal-template",
// };
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
    userToCreate: {},
    page: 1,
    totalUsers: 0,
    searchResultCount: 0,
  },
  created() {
    this.getUsers();
  },
  methods: {
    getUsers(pageNumber = 1) {
      // console.log(pageNumber);
      // console.log(typeof pageNumber);
      this.page = pageNumber;
      fetch(`/api/users?page=${pageNumber}`, {
        method: "GET",
        credentials: "include",
        cache: "no-cache",
        headers: new Headers({
          "content-type": "application/json",
        }),
      })
        .then((response) => response.json())
        .then((json) => {
          // console.log(json.users);
          this.users = json.users;
          this.totalUsers = json.count;
        });
    },
    getToEditUser(toEditID) {
      // const userID = el.id.split("-")[1];
      this.error = "";
      this.showEditModal = true;
      // console.log(toEditID);
      this.userToEdit = this.users.find((obj) => obj.id == toEditID);
      // console.log(this.userToEdit);
    },
    getToDeleteUser(id) {
      // const userID = el.id.split("-")[1];
      this.error = "";
      this.showDeleteModal = true;
      // console.log(id);
      this.userToDelete = this.users.find((obj) => obj.id == id);
      // console.log(this.userToDelete);
    },
    updateUser(email, firstName, lastName) {
      fetch(`/api/users/${this.userToEdit.id}`, {
        method: "PATCH",
        credentials: "include",
        cache: "no-cache",
        body: JSON.stringify({
          email: email,
          first_name: firstName,
          last_name: lastName,
        }),
        headers: new Headers({
          "content-type": "application/json",
        }),
      })
        .then((response) => response.json())
        .then((json) => {
          // console.log(json);
          if (json.success) {
            this.users = this.users.map((obj) =>
              obj.id == this.userToEdit.id ? (obj = json.updated) : (obj = obj)
            );
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
          // console.log(json);
          if (json.success) {
            this.users = this.users.filter((user) => user.id != json.user_id);
            // console.log("users deleted");
            this.users = json.users;
            this.totalUsers = json.count;
            this.showDeleteModal = false;
            this.error = "";
          } else {
            this.error = json.error;
          }
        });
    },
    searchUsers(pageNumber = 1) {
      this.search = this.$refs.userSearch.value;
      this.page = pageNumber;
      fetch(`/api/users?page=${pageNumber}`, {
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
          // console.log(json);
          if (json.success) {
            this.users = json.users;
            this.totalUsers = json.count;
            // this.$refs.userSearch.value = "";
            // console.log("users searched");
          }
        });
    },
    createUser() {
      fetch("/api/users", {
        method: "POST",
        credentials: "include",
        cache: "no-cache",
        body: JSON.stringify({
          email: this.userToCreate.email,
          first_name: this.userToCreate.first_name,
          last_name: this.userToCreate.last_name,
          password: this.userToCreate.password,
        }),
        headers: new Headers({
          "content-type": "application/json",
        }),
      })
        .then((response) => response.json())
        .then((json) => {
          // console.log(json);
          if (json.success) {
            this.totalUsers++;
            this.getUsers(this.pageNumbers.length);
            this.showCreateModal = false;
            this.error = "";
          } else {
            this.error = json.error;
          }
        });
    },
    getPrevious() {
      this.page--;
      if (this.search) {
        this.searchUsers(this.page);
      } else {
        this.getUsers(this.page);
      }
    },
    getNext() {
      this.page++;
      if (this.search) {
        this.searchUsers(this.page);
      } else {
        this.getUsers(this.page);
      }
    },
    getCurrentPage(pageNumber) {
      if (this.search) {
        this.searchUsers(pageNumber);
      } else {
        this.getUsers(pageNumber);
      }
    },
    resetUsers() {
      this.$refs.userSearch.value = "";
      this.getUsers();
    },
    // Configure pagination
    // selectPage(num) {
    //   this.page = num;
    // },
    createUserModal() {
      this.error = "";
      this.showCreateModal = true;
    },
  },
  computed: {
    pageNumbers() {
      let pageNumbers = [];
      let maxPage = Math.ceil(this.totalUsers / 10);
      for (let i = 1; i <= maxPage; i++) {
        pageNumbers.push(i);
      }
      return pageNumbers;
    },
  },
  watch: {
    page() {
      if (this.page < 1) this.page = 1;
      if (this.page > this.pageNumbers.length)
        this.page = this.pageNumbers.length;
    },
  },
});
