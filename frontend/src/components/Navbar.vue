<template>
    <nav class="navbar fixed-top">
        <div class="container">
            <ul class="navbar-nav w-100 d-flex justify-content-start flex-row">
                    <router-link :to="{ name: 'Challenges'}" class="text-white nav-item">
                        <li>
                            <font-awesome-icon icon="fa-solid fa-arrow-left"/>
                        </li>
                    </router-link>
            </ul>
        </div>
    </nav>
</template>