const trips = new Vue({
  components: {
    "create-trip": createTripComponent,
    "edit-trip": editTripComponent,
    "delete-trip": deleteTripComponent,
  },
  el: "#trips",
  delimiters: ["${", "}"],
  data: {
    tripID: null,
    tripToModify: null,
    tripCopy: {},
    trips: {},
    tripsCount: null,
    error: "",
    showCreateModal: false,
    showEditModal: false,
    showDeleteModal: false,
    page: 1,
    searchFlag: false,
    filterTrips: {
      search: "",
      order_by: "id",
      order_type: "asc",
      from_date: null,
      to_date: null,
    },
  },
  methods: {
    showEditTrip(id) {
      this.tripID = id;
      this.tripToModify = this.trips.find((obj) => obj.id == id);
      this.tripCopy = Object.assign({}, this.tripToModify);
      let start_date = new Date(this.tripCopy.start_date);
      let end_date = new Date(this.tripCopy.end_date);
      this.tripCopy.start_date = new Date(
        start_date.getTime() - start_date.getTimezoneOffset() * 60000
      )
        .toISOString()
        .split("T")[0];
      this.tripCopy.end_date = new Date(
        end_date.getTime() - end_date.getTimezoneOffset() * 60000
      )
        .toISOString()
        .split("T")[0];
      this.showEditModal = true;
      // console.log("Trip copy", this.tripCopy);
    },
    getTrips(pageNumber = 1) {
      this.page = pageNumber;
      this.searchFlag = false;
      fetch(`/api/mytrips?page=${pageNumber}`, {
        method: "GET",
        credentials: "include",
        cache: "no-cache",
        headers: new Headers({
          "content-type": "application/json",
        }),
      })
        .then((response) => response.json())
        .then((json) => {
          this.trips = json.trips;
          this.tripsCount = json.count;
        });
    },
    createTripModal() {
      this.error = "";
      this.showCreateModal = true;
    },
    addTrip(destination, startDate, endDate, comment) {
      if (!destination || !startDate || !endDate) {
        this.error = "You have to select destination, start date and end date";
      } else {
        fetch("/api/trips", {
          method: "POST",
          credentials: "include",
          cashe: "no-cashe",
          body: JSON.stringify({
            destination: destination,
            start_date: startDate,
            end_date: endDate,
            comment: comment,
          }),
          headers: new Headers({
            "content-type": "application/json",
          }),
        })
          .then((response) => response.json())
          .then((json) => {
            if (json.success) {
              // console.log("We are in if success");
              this.tripsCount++;
              this.trips.push(json.new_trip);
              this.error = "";
              this.showCreateModal = false;
            } else {
              this.error = json.error;
            }
          });
      }
    },
    editTrip(destination, startDate, endDate, comment) {
      if (!destination || !startDate || !endDate) {
        this.error = "You have to select destination, start date and end date";
      } else {
        fetch(`/api/trips/${this.tripID}`, {
          method: "PUT",
          credentials: "include",
          cashe: "no-cashe",
          body: JSON.stringify({
            destination: destination,
            start_date: startDate,
            end_date: endDate,
            comment: comment,
          }),
          headers: new Headers({
            "content-type": "application/json",
          }),
        })
          .then((response) => response.json())
          .then((json) => {
            if (json.success) {
              // console.log("We are in if Editing");
              this.trips = this.trips.map((obj) =>
                obj.id == this.tripID ? (obj = json.trip) : (obj = obj)
              );
              this.error = "";
              this.showEditModal = false;
            } else {
              this.error = json.error;
            }
          });
      }
    },
    deleteTrip() {
      fetch(`/api/trips/${this.tripID}`, {
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
            this.trips = this.trips.filter(
              (trip) => trip.id != json.deleted_trip_id
            );
            // console.log("users deleted");

            this.tripsCount--;
            this.showDeleteModal = false;
            this.error = "";
          } else {
            this.error = json.error;
          }
        });
    },
    showDeleteTrip(id) {
      this.tripID = id;
      this.showDeleteModal = true;
    },
    searchTrips(pageNumber = 1) {
      this.searchFlag = true;
      this.page = pageNumber;
      fetch(`/api/trips?page=${pageNumber}`, {
        method: "POST",
        credentials: "include",
        cashe: "no-cashe",
        body: JSON.stringify(this.filterTrips),
        headers: new Headers({
          "content-type": "application/json",
        }),
      })
        .then((response) => response.json())
        .then((json) => {
          if (json.success) {
            this.trips = json.trips;
            this.tripsCount = json.count;
          }
        });
    },
    orderBy(column, event) {
      this.searchFlag = true;
      event.preventDefault();
      this.filterTrips.order_by = column;
      // console.log(this.filterTrips.order_by);
      if (this.filterTrips.order_type === "asc") {
        this.filterTrips.order_type = "desc";
      } else {
        this.filterTrips.order_type = "asc";
      }
      this.searchTrips();
    },
    getPrevious() {
      this.page--;
      if (this.searchFlag) {
        this.searchTrips(this.page);
      } else {
        this.getTrips(this.page);
      }
    },
    getNext() {
      this.page++;
      if (this.searchFlag) {
        this.searchTrips(this.page);
      } else {
        this.getTrips(this.page);
      }
    },
    getCurrentPage(pageNumber) {
      if (this.searchFlag) {
        this.searchTrips(pageNumber);
      } else {
        this.getTrips(pageNumber);
      }
    },
  },
  created() {
    this.getTrips();
  },
  computed: {
    pageNumbers() {
      let pageNumbers = [];
      let maxPage = Math.ceil(this.tripsCount / 10);
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
