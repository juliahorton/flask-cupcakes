const $cupcakeList = $('#cupcake-list')
$('#add-cupcake-form').on("submit", handleAddCupcake)

async function handleAddCupcake(e) {
    e.preventDefault()

    let $flavor = $('#flavor').val()
    let $size = $('#size').val()
    let $rating = $('#rating').val()
    let $image = $('#image').val()

    await axios.post(`/api/cupcakes`,{
        flavor: `${$flavor}`,
        size: `${$size}`,
        rating: `${$rating}`,
        image: `${$image}`
    })
    let newLI = `<li>${$size} ${$flavor} cupcake, rated ${$rating}/10</li>`
    $cupcakeList.append(newLI)
    return
}