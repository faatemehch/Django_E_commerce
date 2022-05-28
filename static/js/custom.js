// change(increase or decrease) order detail count
function changeOrderDetailCount(detailId, state) {
    $.get('/order/change_item_counter?detail_id=' + detailId + '&state=' + state).then(res => {
            $('#open-order-content').html(res.body)
        }
    )
}