const { origin, pathname } = window.location;
const baseUrl = origin + pathname;

const searchInput = document.getElementById("search");

const params = new URL(document.location).searchParams;
const offset = params.has("offset") ? parseInt(params.get("offset")) : 0;
const query = params.get("query");

searchInput.value = query;

function redirect(offset = 0, searchKey = "") {
  window.location.href = `${baseUrl}?offset=${offset}&query=${searchKey}`;
}

function goPrev() {
  redirect(offset - 10, query);
}

function goNext() {
  redirect(offset + 10, query);
}

function search() {
  const searchKey = searchInput.value;
  redirect(0, searchKey);
}
