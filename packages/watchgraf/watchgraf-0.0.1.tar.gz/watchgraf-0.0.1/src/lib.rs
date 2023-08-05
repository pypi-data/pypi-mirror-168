use std::{path::Path, sync::{Mutex, Arc}, collections::HashSet, time::Duration, thread::sleep};

use notify::{RecommendedWatcher, Event, event::EventKind::{Create, Modify, Remove }, RecursiveMode, Config, Watcher, Error};
use pyo3::{Python, PyResult, types::PyModule, pyclass, pymethods, pymodule, ToPyObject, PyObject};


#[pyclass]
pub struct WatchGraf {
    watcher: RecommendedWatcher,
    changes: Arc<Mutex<HashSet<String>>>,
    error: Arc<Mutex<Option<String>>>
}

#[pymethods]
impl WatchGraf {
    #[new]
    pub fn new(path: String) -> PyResult<Self> {
        let mut changes: Arc<Mutex<HashSet<String>>> = Arc::new(Mutex::new(HashSet::new()));
        let mut changes_clone = Arc::clone(&changes);
        
        let mut error: Arc<Mutex<Option<String>>> = Arc::new(Mutex::new(None));
        let mut error_clone = Arc::clone(&error);

        let event_handler = move |result: notify::Result<Event>| {
            match result {
                Ok(event) => {
                    let path_buf = event.paths.first();
                    if let None = path_buf{
                        return
                    }
                    let path_buf = path_buf.unwrap();

                    let path = match path_buf.to_str() {
                        Some(s) => s.to_string(),
                        None => return,
                    };

                    match event.kind {
                        Create(_) | Modify(_) | Remove(_) => {
                            changes_clone.lock().unwrap().insert(path);  
                            ()
                        },
                        _ => ()

                    }
                }
                Err(e) => {
                    println!("watch error {:?}", e);
                    *error_clone.lock().unwrap() = Some(e.to_string());
                }
            }        
        };
        let mut watcher: RecommendedWatcher = RecommendedWatcher::new(event_handler, Config::default()).unwrap();
        watcher.watch(Path::new(&path), RecursiveMode::Recursive);
        Ok(WatchGraf{watcher, changes, error})

    }

    pub fn watch(&self, py: Python) -> PyResult<PyObject>{
        let sleep_time = Duration::from_millis(500);
        py.allow_threads(|| sleep(sleep_time));
        let size = self.changes.lock().unwrap().len();
        if size > 0 {
            let new_paths = self.changes.lock().unwrap().clone();
            self.clear();
            return Ok(new_paths.to_object(py));
        }

        return Ok(().to_object(py));
    }

    fn clear(&self) {
        self.changes.lock().unwrap().clear();
    }
}

#[pymodule]
fn _watchgrafrs(py: Python, m: &PyModule) -> PyResult<()> {
    m.add_class::<WatchGraf>()?;
    Ok(())
}