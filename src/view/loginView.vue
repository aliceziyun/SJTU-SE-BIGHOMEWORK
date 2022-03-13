<template>
    <div style="text-align:center">
        <login-window></login-window>
    </div>
</template>

<script>
import loginWindow from "../components/loginWindow.vue"

export default {
    name: "loginView",
    components: {
        loginWindow
    }
}
</script>