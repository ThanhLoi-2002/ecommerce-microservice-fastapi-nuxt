export const formatPrice = (price?: number): string => {
    return new Intl.NumberFormat('vi-VN', { style: 'currency', currency: 'VND' }).format(price ? price : 0);
};

export const formatTime = (date: Date): string => {
    return date.toLocaleTimeString('vi-VN', { hour: '2-digit', minute: '2-digit' });
};