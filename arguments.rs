use std::env;
use std::error::Error;
use std::fs::File;
use std::io::prelude::*;
use std::path::Path;

// HACER UNA FUNCION PARA CREAR ARCHIVO
// HACER UNA FUNCION PARA ESCRIBIR ARCHIVO
// HACER FUNCIONAR PARA ENCRIPTAR ARCHIVO
// HACER FUNCIONAR PARA DESENCRIPTAR ARCHIVO

fn main() {
  let args : Vec<String> = env::args().collect();

  println!("This is the program path {}", args[0]);    
  println!("This is the file path {}", args[1]);

  // Create a path to the desired file
  let path = Path::new(&args[1]);
  let display = path.display();

  // Open the path in read-only mode, returns `io::Result<File>`
  let mut file = match File::open(&path) {
      // The `description` method of `io::Error` returns a string that
      // describes the error
      Err(why) => panic!("couldn't open {}: {}", display,
                                                 Error::description(&why)),
      Ok(file) => file,
  };

  // SHOULD READ FILE CONTENT INTO BIT VECTOR TO ENCRYPT AND DECRYPT
  // let mut s = String::new();
  // match file.read_to_string(&mut s) {
  //     Err(why) => panic!("couldn't read {}: {}", display,
  //                                                Error::description(&why)),
  //     Ok(_) => print!("{} contains:\n{}", display, s),
  // }

  // Open a file in write-only mode, returns `io::Result<File>`
  let encrypted_path = "encrypted".to_string() + &args[1];
  let mut encrypted_file = match File::create(&encrypted_path) {
      Err(why) => panic!("couldn't create {}: {}",
                         display,
                         Error::description(&why)),
      Ok(encrypted_file) => encrypted_file,
  };

  match encrypted_file.write_all("probando encrypted".as_bytes()) {
      Err(why) => {
          panic!("couldn't write to {}: {}", display,
                                             Error::description(&why))
      },
      Ok(_) => println!("successfully wrote to {}", display),
  }

  let decrypted_path = "decrypted".to_string() + &args[1];
  let mut decrypted_file = match File::create(&decrypted_path) {
      Err(why) => panic!("couldn't create {}: {}",
                         display,
                         Error::description(&why)),
      Ok(decrypted_file) => decrypted_file,
  };

  match decrypted_file.write_all("probando decrypted".as_bytes()) {
      Err(why) => {
          panic!("couldn't write to {}: {}", display,
                                             Error::description(&why))
      },
      Ok(_) => println!("successfully wrote to {}", display),
  }
}