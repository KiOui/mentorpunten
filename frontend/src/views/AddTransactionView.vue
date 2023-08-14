<script setup lang="ts">
import Header from "@/components/Header.vue";
import {computed, onMounted, ref} from "vue";
import useApiService from "@/common/api.service";
import type Team from "@/models/team.model";
import type Tournament from "@/models/tournament.model";
import User from "@/models/user.model";
import {useToast} from "vue-toastification";

const tournaments = ref<Tournament[] | null>(null);
const teams = ref<Team[] | null>(null);

const loadingAmount = ref<boolean | null>(true);

const ApiService = useApiService();
const user = ref<User | null>(null);
const toast = useToast();

const form = ref<HTMLFormElement | null>(null);

onMounted (() => {
    ApiService.getTournaments().then(result => {
        tournaments.value = result;
    }).catch(() => {
        tournaments.value = null;
    });
    ApiService.getUsersMe().then(result => {
        user.value = result;
    }).catch(() => {
        user.value = null;
    });
});

function findTeams(event: Event): void {
    const htmlInputEvent = event.target as HTMLInputElement;
    const tournamentId = htmlInputEvent.value;
    ApiService.getChallengesTeams(new URLSearchParams([['tournament', String(tournamentId)]]))
        .then(result => {
            teams.value = result;
        }).catch(() => {
            teams.value = null;
        });
}

function loadButton(event: Event): void {
    const htmlInputEvent = event.target as HTMLInputElement;
    const description = htmlInputEvent.value;
    if (description !== "") {
        loadingAmount.value = false;
    }
}

function submitTransaction(event: Event) {
    event.preventDefault();
    console.log(user.value);
    if (user.value === null){
        return;
    } else {
        const form = document.getElementById("transaction") as HTMLFormElement;
        const formData = new FormData(form);
        const data = Object.fromEntries(formData.entries());
        const requestData = new FormData();
        requestData.append("account", data.team);
        requestData.append("amount", data.amount);
        requestData.append("description", data.description);
        requestData.append("processor", user.value.id);
        ApiService.postTransaction(requestData).then(() => {
            toast.success("Transaction uploaded successfully!");
            form.reset();
        }).catch(() => {
            toast.error("Transaction upload failed!");
        });
    }
}

</script>

<template>
<Header :show-back-button="true"/>
<div class="custom-card feed-container mx-auto">
    <h1>add transaction</h1>
    <form class="row custom-form" id="transaction" v-on:submit="submitTransaction($event)" ref="form">
        <select id="tournament" name="tournament" v-on:change="findTeams($event)">
            <optgroup>
                <option value="" disabled selected class="custom-option">Select tournament</option>
                <option v-for="tournament in tournaments" :value="tournament.id" class="custom-option">{{ tournament.name }}</option>
            </optgroup>
        </select>
        <select id="team" name="team">
            <optgroup>
                <option value="" disabled selected class="custom-option">Select team</option>
                <option v-for="team in teams" :value="team.id" class="custom-option">{{ team.name }}</option>
            </optgroup>
        </select>
        <input type="number" id="amount" name="amount" placeholder="amount">
        <input type="text" id="description" name="description" placeholder="description" v-on:change="loadButton($event)">
        <button v-if="!loadingAmount" type="submit" value="Submit" class="btn btn-primary">submit</button>
        <button v-else type="submit" value="Submit" class="btn btn-primary disabled">submit</button>
    </form>
</div>
</template>

<style>
.custom-form {
    flex-direction: column;
    align-items: center;
    justify-content: center;
    width: 100%;
}

.custom-form select {
    margin-bottom: 1rem;
    outline: none;
    font-family: 'Open Sans Condensed';
    text-transform: uppercase;
    border-radius: 0.25rem;
    border: solid 1px #d9d9d9;
}

.custom-form input:focus {
    outline: solid 2px var(--primary);
}

.custom-form input {
    font-family: 'Open Sans Condensed';
    text-transform: uppercase;
    margin-bottom: 1rem;
    border-radius: 0.25rem;
    border: solid 1px #d9d9d9;
}

.custom-form input:focus {
    outline: solid 2px var(--primary);
}

.custom-form button {
    width: fit-content;
}
</style>