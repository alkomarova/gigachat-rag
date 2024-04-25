<script setup lang="ts">
import Sidebar from './components/Sidebar.vue'
import ChatInput from './components/ChatInput.vue'
import ChatMessages from './components/ChatMessages.vue'
import Settings from './components/Settings.vue'
import ModelSelector from './components/ModelSelector.vue'
import { isDarkMode, isSettingsOpen } from './services/appConfig.ts'
import { onMounted, ref } from 'vue'
import { useAI } from './services/useAI.ts'
import { useChats } from './services/chat.ts'
import TextInput from './components/Inputs/TextInput.vue'

const { refreshModels, availableModels } = useAI()
const { activeChat, renameChat, switchModel, initialize } = useChats()
const isEditingChatName = ref(false)
const editedChatName = ref('')

const startEditing = () => {
  isEditingChatName.value = true
  editedChatName.value = activeChat.value?.name || ''
}

const cancelEditing = () => {
  isEditingChatName.value = false
  editedChatName.value = ''
}

const confirmRename = () => {
  if (activeChat.value && editedChatName.value) {
    renameChat(editedChatName.value)
    isEditingChatName.value = false
  }
}

</script>

<template>
  <div :class="{ dark: isDarkMode }">
    <main
      class="flex h-full w-full flex-1 flex-row items-stretch bg-zinc-50 dark:bg-zinc-800"
    >
      <Sidebar />

      <div class="mx-auto flex h-[100vh] w-full flex-col">
        <div class="mx-auto flex h-[100vh] w-full max-w-7xl flex-col gap-4 px-4 pb-4">
          <div
            class="flex w-full flex-row items-center justify-center gap-4 rounded-b-xl bg-zinc-200 px-4 py-2 dark:bg-zinc-700"
          >
            <div class="mr-auto flex h-full items-center" v-if="activeChat">
              <div>
                <div v-if="isEditingChatName">
                  <TextInput
                    autofocus
                    v-model="editedChatName"
                    @keyup.enter="confirmRename"
                    @keyup.esc="cancelEditing"
                    @blur="cancelEditing"
                  />
                </div>
              </div>
            </div>

          </div>

          <ChatMessages />
          <ChatInput />
        </div>
      </div>
    </main>
  </div>
</template>
