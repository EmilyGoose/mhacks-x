export const state = () => ({
  tokens: []
})

export const mutations = {
  setTokens (state, tokens) {
    state.tokens = tokens
  }
}
