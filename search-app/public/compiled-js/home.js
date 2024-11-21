import axios from 'axios';
const navbarApp = Vue.createApp({
    data() {
        return {
            isDropdownOpen: false, // State to manage dropdown visibility
            basicSearch: "",
            methodSearch: null,
            language: "latin",
            variant: "zero",
            volumes: [],
            pageSearch: "",
            entrySearch: "",
            startDate: "",
            endDate: "",
            docId: "",

        };
    },
    methods: {
        toggleDropdown() {
            this.isDropdownOpen = !this.isDropdownOpen; // Toggle dropdown visibility
        },
        dataStored(){
            const dataUser = {
                basicSearch: this.basicSearch,
                methodSearch: this.methodSearch,
                language: this.language,
                variant: this.variant,
                volumes: this.volumes,
                pageSearch: this.pageSearch,
                entrySearch: this.entrySearch,
                startDate: this.startDate,
                endDate: this.endDate,
                docId: this.docId,
            };

            axios.post('/search', dataUser)
            .then(response => {
                // Handle successful response, like showing results
                console.log(response.data);
            })
            .catch(error => {
                console.error(error);
            });
        }
    },
});
//cponsistent key names:  the
navbarApp.mount("#advanced");
