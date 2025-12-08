export function useForm() {
    function syncForm(target: any, source: any) {
        if (!source) return

        Object.keys(target).forEach(key => {
            if (source[key] !== undefined) {
                target[key] = source[key];
            }
        });
    }
    
    return {
        syncForm
    }
}