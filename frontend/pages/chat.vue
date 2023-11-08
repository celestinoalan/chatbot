<template>
  <bubble-chat :messages="messages" />
</template>

<script>
import BubbleChatVue from "../components/BubbleChat.vue";

export default {
  components: [BubbleChatVue],

  data() {
    return {
      messages: [
        // {
        //   text: "Teste 1",
        //   name: "Usuário 1",
        //   avatar: "link-para-o-avatar-1.jpg",
        // },
        // {
        //   text: "Teste 2",
        //   name: "Usuário 2",
        //   avatar: "link-para-o-avatar-2.jpg",
        // },
        // {
        //   text: "Teste 3",
        //   name: "me",
        //   avatar: "link-para-o-avatar-3.jpg",
        //   isMine: true,
        // },
      ],
    };
  },
};
</script>

<style>
</style>