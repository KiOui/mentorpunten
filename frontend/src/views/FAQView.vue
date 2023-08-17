<script setup lang="ts">
import Header from '@/components/Header.vue'
import { ref } from 'vue'

const faq = ref<{}>({})

let questionDictionary = [
    { 
        question: "How can I be placed in a team?", 
        answer: "You can be placed in a team by a member of the Introcie after you have logged in."
    },
    { 
        question: "Are points and coins the same?", 
        answer: "No. Points are used to determine the winner of a tournament. Coins are used to buy items in the shop."
    },
];

faq.value = questionDictionary;

</script>

<template>
    <Header :show-back-button="true" />
    <div class="feed-container mx-auto">
        <div class="custom-card">
            <h1>F.A.Q.</h1>
        </div>
        <div class="accordion accordion-flush" id="accordionFlushExample">
            <div class="accordion-item">
                <h2 class="accordion-header">
                    <button class="accordion-button collapsed" type="button" data-bs-toggle="collapse" data-bs-target="#flush-collapseOne" aria-expanded="false" aria-controls="flush-collapseOne">
                        How can I be placed in a team?
                    </button>
                </h2>
                <div id="flush-collapseOne" class="accordion-collapse collapse" data-bs-parent="#accordionFlushExample">
                    <div class="accordion-body">
                        You can be placed in a team by a member of the Introcie after you have logged in.
                    </div>
                </div>
            </div>
            <div class="accordion-item">
                <h2 class="accordion-header">
                    <button class="accordion-button collapsed" type="button" data-bs-toggle="collapse" data-bs-target="#flush-collapseTwo" aria-expanded="false" aria-controls="flush-collapseTwo">
                        Are points and coins the same?
                    </button>
                </h2>
                <div id="flush-collapseTwo" class="accordion-collapse collapse" data-bs-parent="#accordionFlushExample">
                    <div class="accordion-body">
                        No. Points are used to determine the winner of a tournament. Coins are used to buy items in the shop.
                    </div>
                </div>
            </div>
            <div class="accordion-item">
                <h2 class="accordion-header">
                    <button class="accordion-button collapsed" type="button" data-bs-toggle="collapse" data-bs-target="#flush-collapseThree" aria-expanded="false" aria-controls="flush-collapseThree">
                        Does a challenge need to be completed with your whole team?
                    </button>
                </h2>
                <div id="flush-collapseThree" class="accordion-collapse collapse" data-bs-parent="#accordionFlushExample">
                    <div class="accordion-body">
                        No. You can complete a challenge with as many people as you want.
                    </div>
                </div>
            </div>
            <div class="accordion-item">
                <h2 class="accordion-header">
                    <button class="accordion-button collapsed" type="button" data-bs-toggle="collapse" data-bs-target="#flush-collapseFour" aria-expanded="false" aria-controls="flush-collapseFour">
                        Is there a time limit for submissions of the challenges?
                    </button>
                </h2>
                <div id="flush-collapseFour" class="accordion-collapse collapse" data-bs-parent="#accordionFlushExample">
                    <div class="accordion-body">
                        That depends. Some challenges have a limit, but that limit is always stated in the challenge description. If there is no limit stated, you can submit your challenge until the end of the tournament.
                    </div>
                </div>
            </div>
            <div class="accordion-item">
                <h2 class="accordion-header">
                    <button class="accordion-button collapsed" type="button" data-bs-toggle="collapse" data-bs-target="#flush-collapseFive" aria-expanded="false" aria-controls="flush-collapseFive">
                        Can you complete alcohol challenges with non-alcoholic drinks?
                    </button>
                </h2>
                <div id="flush-collapseFive" class="accordion-collapse collapse" data-bs-parent="#accordionFlushExample">
                    <div class="accordion-body">
                        Yes, but only with alcohol free beer.
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<style scoped>
.accordion-button:not(.collapsed) {
    color: var(--primary) !important;
    background-color: white !important;
}

.accordion-body {
    font-style: italic;
}
</style>