#[macro_export]
macro_rules! new_rc {
    ($pub:vis fn $fname:ident($($arg:ident : $argtype:ty),* $(,)?) -> ($rettype:ty)  $body:expr)=>{
        $pub fn $fname($($arg : $argtype),*)->$rettype {
            $body
        }

        pub fn nrc($($arg : $argtype),* )->CircuitRc{
            Self::$fname($($arg),* ).rc()
        }
    }
}
#[macro_export]
macro_rules! new_rc_unwrap {
    ($pub:vis fn $fname:ident($( $arg:ident : $argtype:ty),* $(,)?) -> ($rettype:ty)  $body:expr)=>{
        $pub fn $fname($($arg : $argtype),*)->$rettype {
            $body
        }

        pub fn nrc($($arg : $argtype),*)->CircuitRc{
            Self::$fname($($arg),*).unwrap().rc()
        }
    }
}

// #[apply(new_rc)]
// pub fn tempty(x:usize)->(usize){
//     0
// }
