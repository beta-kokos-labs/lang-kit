function hi( name){
    console.log('hi');
    console.error('errir');
    console.log('done');
    // hello( name)
    if( name =='Ethan' && name !=='jo') //'--' is &&,'|' is || && not is'!'
    {
    console.log('hi Ethan')
    }
    else if( name !=='Ethan' && name !=='jo')
    {
    console.log('imposter')
    }
    else{
    console.log('hi jo')
    }
    }
    hi('Ethan')
    hi('jo')
    hi('michal')
    console.log('complete')