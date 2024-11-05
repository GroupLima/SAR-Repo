const navbarApp = Vue.createApp({
    data() {
        return {
            isDropdownOpen: false, // State to manage dropdown visibility
        };
    },
    methods: {
        toggleDropdown() {
            this.isDropdownOpen = !this.isDropdownOpen; // Toggle dropdown visibility
        },
    },
});

navbarApp.mount("#advanced");
